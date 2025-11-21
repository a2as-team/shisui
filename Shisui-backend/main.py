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

            async for event in runner.run_async(
                user_id=request.user_id,
                session_id=session_id,
                new_message=Content(role='user', parts=[Part(text=request.message)]),
                run_config=RunConfig(streaming_mode=StreamingMode.SSE),
            ):
                # Check for agent delegation
                if hasattr(event, 'author') and event.author != 'planner_agent':
                    agent_author_str = event.author.lower()
                    if 'course' in agent_author_str:
                        current_agent_name = 'course'
                        current_agent_display = 'Course Agent'
                    elif 'exam' in agent_author_str:
                        current_agent_name = 'exam'
                        current_agent_display = 'Exam Agent'
                    
                    if current_agent_name:
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
                        
                        elif hasattr(part, 'text') and part.text and event.partial:
                            content = part.text
                            chunk_data = {
                                'type': 'content',
                                'content': content,
                                'agent_name': current_agent_name,
                                'agent_display': current_agent_display
                            }
                            yield f"data: {json.dumps(chunk_data)}\n\n"
            
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
