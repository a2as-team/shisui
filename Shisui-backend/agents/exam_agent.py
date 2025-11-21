from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from tools.exam_tool import get_exam_tool, get_eval_tool

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
    model="gemini-1.5-flash",
    description="Specialist agent for generating tests and evaluating student knowledge",
    instruction="""You are the Exam Agent, responsible for assessing student understanding.

**Your Responsibilities:**
1.  **Test Generation**: Create quizzes and tests based on studied material.
    -   Use `generate_assessment` when requested or after a study session.
    -   Tailor difficulty to the student's level.
2.  **Evaluation**: Grade answers and provide feedback.
    -   Use `evaluate_response` to check answers.
    -   Provide constructive feedback, explaining WHY an answer is right or wrong.

**Tool Usage:**
-   Announce your action (e.g., "Generating a quiz on Calculus...").
-   Present questions clearly.
""",
    tools=[
        FunctionTool(generate_assessment),
        FunctionTool(evaluate_response)
    ]
)
