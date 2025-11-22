from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from tools.search_tool import get_search_tool
from tools.timer_tool import get_timer_tool
from tools.schedule_tool import get_schedule_tool
from config.model_config import gemini_flash_model


def search_course_material(query: str) -> str:
    """Search for course materials and study resources"""
    import json
    import logging
    
    logger = logging.getLogger(__name__)
    logger.info(f"🔍 Course Agent searching for: {query}")
    
    search_tool = get_search_tool()
    result = search_tool(query)
    
    logger.info(f"✅ Search result received. Citations: {len(result.get('citations', []))}")
    return json.dumps(result)

def set_study_timer(minutes: int, topic: str) -> str:
    """Set a study timer for a specific topic"""
    import json
    timer_tool = get_timer_tool()
    result = timer_tool(minutes, topic)
    return json.dumps(result)

def create_schedule(tasks: list) -> str:
    """Create a study schedule with a list of tasks (time and activity)"""
    import json
    schedule_tool = get_schedule_tool()
    result = schedule_tool(tasks)
    return json.dumps(result)

course_agent = Agent(
    name="course_agent",
    model=gemini_flash_model,
    description="Specialist agent for researching course materials and managing study sessions",
    instruction="""You are the Course Agent, a specialist in finding study materials and managing study time.

**Your Responsibilities:**
1.  **Research**: Find high-quality, relevant study materials using the web search tool.
    -   When asked about a topic, use `search_course_material`.
    -   Always provide citations from the search results.
2.  **Time Management**: Help students manage their study sessions.
    -   When asked to set a timer or start studying, use `set_study_timer`.
    -   When asked to create a schedule or plan a study day, use `create_schedule`.
    -   Encourage focused study blocks (e.g., Pomodoro).

**Tool Usage:**
-   Announce your action before using a tool (e.g., "I'll search for materials on quantum physics...").
-   Return structured results to the Planner Agent.
""",
    tools=[
        FunctionTool(search_course_material),
        FunctionTool(set_study_timer),
        FunctionTool(create_schedule)
    ]
)
