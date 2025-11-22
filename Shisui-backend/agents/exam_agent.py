from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from tools.exam_tool import get_exam_tool, get_eval_tool
from config.model_config import gemini_flash_model


def generate_assessment(topic: str, difficulty: str = "medium", num_questions: int = 5) -> str:
    """Generate a test/assessment for a topic"""
    import json
    exam_tool = get_exam_tool()
    result = exam_tool(topic, difficulty, num_questions)
    return json.dumps(result)

def evaluate_response(question: str, user_answer: str, correct_answer: str) -> str:
    """Evaluate a student's answer"""
    import json
    eval_tool = get_eval_tool()
    result = eval_tool(question, user_answer, correct_answer)
    return json.dumps(result)

exam_agent = Agent(
    name="exam_agent",
    model=gemini_flash_model,
    description="Specialist agent for generating tests and evaluating student knowledge",
    instruction="""You are the Exam Agent, responsible for assessing student understanding.

**Your Capabilities:**
1.  **Test Generation**: Create quizzes and tests based on studied material.
    -   Use `generate_assessment` when requested or after a study session.
    -   Tailor difficulty to the student's level.
2.  **Evaluation**: Grade answers and provide feedback.
    -   Use `evaluate_response` to check answers.
    -   Provide constructive feedback, explaining WHY an answer is right or wrong.

**What You CANNOT Do:**
-   Set study timers (Course Agent handles this)
-   Search for study materials or resources (Course Agent handles this)
-   Create study schedules (Course Agent handles this)
-   Access student history or general planning (Planner Agent handles this)

**Important - Transfer Back:**
-   If asked to do something outside your capabilities, politely explain what you cannot do and use `transfer_back` to return control to the Planner Agent.
-   Example: "I can't set timers, but I can help test your knowledge. Let me transfer you back to the planner to set up a timer for you."

**Tool Usage:**
-   Announce your action (e.g., "Generating a quiz on Calculus...").
-   Present questions clearly.
""",
    tools=[
        FunctionTool(generate_assessment),
        FunctionTool(evaluate_response)
    ]
)
