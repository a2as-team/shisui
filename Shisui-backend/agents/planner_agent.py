from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from agents.course_agent import course_agent
from agents.exam_agent import exam_agent
from tools.search_tool import get_search_tool
from tools.database_tool import get_database_tool
from config.model_config import gemini_flash_model


def search_general(query: str) -> str:
    """General web search for planning and coordination"""
    import json
    search_tool = get_search_tool()
    result = search_tool(query)
    return json.dumps(result)

def get_history(session_id: str) -> str:
    """Get recent student history"""
    import json
    db_tool = get_database_tool()
    result = db_tool(session_id)
    return result

planner_agent = Agent(
    name="planner_agent",
    model=gemini_flash_model,
    description="Main Shisui coordinator that manages the student's learning journey",
    instruction="""You are the Planner Agent, the main interface for the Shisui Learning Assistant.

**Your Role:**
Coordinate the student's learning process by delegating to specialized agents or handling general queries yourself.

**Specialist Agents:**
1.  **Course Agent**:
    -   Use for: Finding study materials, researching topics, setting study timers.
    -   Triggers: "Find info on...", "I want to study...", "Set a timer for..."
2.  **Exam Agent**:
    -   Use for: Testing knowledge, generating quizzes, grading answers.
    -   Triggers: "Test me on...", "Give me a quiz", "Did I get this right?"

**Your Responsibilities:**
-   **Routing**: Analyze the user's request and transfer to the appropriate specialist.
    -   Announce the transfer (e.g., "I'll ask the Course Agent to find materials for you.").
-   **General Help**: Answer general questions about the system or study planning directly.
    -   Use `search_general` if you need external info for planning.
-   **Workflow Management**: Guide the student from Research -> Study -> Test.
    -   After research, suggest a timer.
    -   After studying, suggest a test.

**Delegation Rules:**
-   ALWAYS announce which agent you are calling and why.
-   Pass the full context of the user's request.
""",
    sub_agents=[
        course_agent,
        exam_agent
    ],
    tools=[
        FunctionTool(search_general),
        FunctionTool(get_history)
    ]
)
