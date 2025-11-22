import os
import json
import uuid
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from google.adk.agents.run_config import RunConfig, StreamingMode
from agents.planner_agent import planner_agent
from tools.database_tool import init_db, log_interaction


# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Shisui Backend")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create reports directory if it doesn't exist
REPORTS_DIR = os.path.join(os.path.dirname(__file__), 'reports')
os.makedirs(REPORTS_DIR, exist_ok=True)

# Mount reports directory
app.mount("/reports", StaticFiles(directory=REPORTS_DIR), name="reports")

# Initialize session service
session_service = InMemorySessionService()

# Initialize database (DISABLED - uncomment when MySQL is set up)
# try:
#     logger.info("Initializing database connection...")
#     init_db()
#     logger.info("✓ Database initialized successfully")
# except Exception as e:
#     logger.error(f"✗ Database initialization failed: {e}")
#     logger.warning("App will continue but database features may not work")


class ChatRequest(BaseModel):
    message: str
    user_id: str = "default_user"
    session_id: Optional[str] = None

@app.get("/")
async def root():
    return {"status": "Shisui System Online"}

@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Chat endpoint that streams responses from the Planner Agent.
    """
    async def generate_stream():
        try:
            session_id = request.session_id or str(uuid.uuid4())
            yield f"data: {json.dumps({'type': 'session', 'session_id': session_id})}\n\n"

            # Ensure session exists
            session = await session_service.get_session(
                app_name="shisui_app",
                user_id=request.user_id,
                session_id=session_id
            )
            if not session:
                session = await session_service.create_session(
                    app_name="shisui_app",
                    user_id=request.user_id,
                    session_id=session_id,
                    state={}
                )

            runner = Runner(
                agent=planner_agent,
                app_name="shisui_app",
                session_service=session_service
            )

            current_agent_name = None
            current_agent_display = None
            full_response = ""  # Collect full response for database logging
            pending_citations = [] # Buffer for citations

            async for event in runner.run_async(
                user_id=request.user_id,
                session_id=session_id,
                new_message=Content(role='user', parts=[Part(text=request.message)]),
                run_config=RunConfig(streaming_mode=StreamingMode.SSE),
            ):
                # Handle agent switching
                # Check if event has author attribute (it should for agent turns)
                if hasattr(event, 'author') and event.author:
                    # If author changed, update current agent
                    if event.author != current_agent_name:
                        current_agent_name = event.author
                        
                        # Map internal name to display name
                        display_map = {
                            "planner_agent": "Planner Agent",
                            "course_agent": "Course Agent",
                            "exam_agent": "Exam Agent",
                            "user": "User"
                        }
                        
                        # Only notify if it's an agent (not user)
                        if current_agent_name != "user":
                            current_agent_display = display_map.get(current_agent_name, current_agent_name)
                            
                            agent_data = {
                                'type': 'agent_working',
                                'agent_name': current_agent_name,
                                'agent_display': current_agent_display
                            }
                            yield f"data: {json.dumps(agent_data)}\n\n"
                            logger.info(f"🤖 Sub-agent working: {current_agent_display}")

                # Handle content and tool calls
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, 'function_call') and part.function_call:
                            tool_name = part.function_call.name
                            tool_data = {
                                'type': 'tool_call',
                                'tool_name': tool_name
                            }
                            yield f"data: {json.dumps(tool_data)}\n\n"
                            logger.info(f"🔧 Tool call detected: {tool_name}")
                        
                        # Check for function response (tool results)
                        elif hasattr(part, 'function_response') and part.function_response:
                            func_response = part.function_response
                            
                            # Check if it's a timer response
                            try:
                                response_data = json.loads(func_response.response.get('result', '{}'))
                                
                                # Handle Timer
                                if response_data.get('action') == 'start_timer':
                                    timer_event = {
                                        'type': 'timer_start',
                                        'duration_minutes': response_data.get('duration_minutes'),
                                        'label': response_data.get('label'),
                                        'message': response_data.get('message')
                                    }
                                    yield f"data: {json.dumps(timer_event)}\n\n"
                                    logger.info(f"⏱️ Timer started: {response_data.get('duration_minutes')} min")
                                
                                # Handle Citations (Buffer them)
                                if response_data.get('citations'):
                                    pending_citations.extend(response_data.get('citations'))
                                    logger.info(f"📚 Citations buffered: {len(response_data.get('citations'))}")
                                    
                            except:
                                pass
                        
                        elif hasattr(part, 'text') and part.text and event.partial:
                            content = part.text
                            full_response += content  # Collect response
                            chunk_data = {
                                'type': 'content',
                                'content': content,
                                'agent_name': current_agent_name,
                                'agent_display': current_agent_display
                            }
                            yield f"data: {json.dumps(chunk_data)}\n\n"
            
            # Send buffered citations at the end
            if pending_citations:
                citations_event = {
                    'type': 'citations',
                    'citations': pending_citations
                }
                yield f"data: {json.dumps(citations_event)}\n\n"
                logger.info(f"📚 Sending {len(pending_citations)} citations to frontend")

            yield f"data: {json.dumps({'type': 'done'})}\n\n"


        except Exception as e:
            logger.error(f"Error in streaming chat: {str(e)}")
            error_data = {'type': 'error', 'error': str(e)}
            yield f"data: {json.dumps(error_data)}\n\n"

    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
