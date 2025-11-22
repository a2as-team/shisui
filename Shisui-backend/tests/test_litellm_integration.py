"""
Test LiteLLM + OpenRouter integration with ADK agents
"""
import sys
import os
import asyncio

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.model_config import gemini_flash_model, get_model_by_alias, MODELS
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.genai.types import Content, Part


def test_model_configuration():
    """Test that model configuration is set up correctly"""
    print("="*60)
    print("Test 1: Model Configuration")
    print("="*60)
    
    try:
        # Test default model
        print(f"\n[SUCCESS] Default model loaded: {gemini_flash_model.model}")
        
        # Test model aliases
        print(f"\nAvailable model aliases:")
        for alias, model_id in MODELS.items():
            print(f"  - {alias}: {model_id}")
        
        # Test getting model by alias
        test_model = get_model_by_alias("gemini-flash")
        print(f"\n[SUCCESS] Retrieved model by alias: {test_model.model}")
        
        return True
    except Exception as e:
        print(f"\n[ERROR] Model configuration failed: {str(e)}")
        return False


def simple_tool_function(message: str) -> str:
    """A simple test tool"""
    return f"Tool received: {message}"


async def test_agent_with_litellm():
    """Test creating and running an agent with LiteLLM model"""
    print("\n" + "="*60)
    print("Test 2: Agent with LiteLLM Model")
    print("="*60)
    
    try:
        # Create a simple test agent
        test_agent = Agent(
            name="test_agent",
            model=gemini_flash_model,
            description="Test agent using LiteLLM with OpenRouter",
            instruction="You are a helpful test assistant. Answer questions concisely.",
            tools=[FunctionTool(simple_tool_function)]
        )
        
        print(f"\n[SUCCESS] Created agent with model: {test_agent.model.model}")
        print(f"Agent name: {test_agent.name}")
        print(f"Agent description: {test_agent.description}")
        
        return True
    except Exception as e:
        print(f"\n[ERROR] Agent creation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_agent_response():
    """Test getting a response from an agent using OpenRouter"""
    print("\n" + "="*60)
    print("Test 3: Agent Response via OpenRouter")
    print("="*60)
    
    try:
        from google.adk.runners import Runner
        from google.adk.sessions import InMemorySessionService
        
        # Create session service
        session_service = InMemorySessionService()
        
        # Create test agent
        test_agent = Agent(
            name="test_agent",
            model=gemini_flash_model,
            description="Test agent",
            instruction="You are a helpful assistant. Answer in one short sentence."
        )
        
        # Create runner
        runner = Runner(
            agent=test_agent,
            app_name="test_app",
            session_service=session_service
        )
        
        print("\n[INFO] Sending test message to agent...")
        print("Question: 'What is 2+2? Answer in one sentence.'")
        
        # Create session
        session = await session_service.create_session(
            app_name="test_app",
            user_id="test_user",
            session_id="test_session",
            state={}
        )
        
        # Run agent
        response_text = ""
        async for event in runner.run_async(
            user_id="test_user",
            session_id="test_session",
            new_message=Content(role='user', parts=[Part(text="What is 2+2? Answer in one sentence.")])
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        response_text += part.text
        
        print(f"\n[SUCCESS] Agent response received:")
        print(f"Response: {response_text}")
        
        return True
    except Exception as e:
        print(f"\n[ERROR] Agent response test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_actual_agents():
    """Test the actual Shisui agents with LiteLLM"""
    print("\n" + "="*60)
    print("Test 4: Actual Shisui Agents")
    print("="*60)
    
    try:
        # Import actual agents
        from agents.planner_agent import planner_agent
        from agents.course_agent import course_agent
        from agents.exam_agent import exam_agent
        
        agents = [
            ("Planner Agent", planner_agent),
            ("Course Agent", course_agent),
            ("Exam Agent", exam_agent)
        ]
        
        print("\n[INFO] Checking agent configurations...")
        for name, agent in agents:
            print(f"\n{name}:")
            print(f"  - Model: {agent.model.model}")
            print(f"  - Tools: {len(agent.tools) if agent.tools else 0}")
            print(f"  - Sub-agents: {len(agent.sub_agents) if agent.sub_agents else 0}")
        
        print("\n[SUCCESS] All agents configured with LiteLLM + OpenRouter")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Agent configuration check failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def run_all_tests():
    """Run all integration tests"""
    print("\n" + "="*70)
    print(" LiteLLM + OpenRouter + ADK Integration Tests")
    print("="*70)
    
    results = []
    
    # Test 1: Model configuration
    results.append(("Model Configuration", test_model_configuration()))
    
    # Test 2: Agent creation
    results.append(("Agent Creation", await test_agent_with_litellm()))
    
    # Test 3: Agent response (this will use API credits)
    print("\n[INFO] Test 3 will make an actual API call to OpenRouter...")
    user_input = input("Continue with API test? (y/n): ")
    if user_input.lower() == 'y':
        results.append(("Agent Response", await test_agent_response()))
    else:
        print("[SKIPPED] Agent response test")
        results.append(("Agent Response", None))
    
    # Test 4: Actual agents
    results.append(("Actual Agents", await test_actual_agents()))
    
    # Summary
    print("\n" + "="*70)
    print(" Test Summary")
    print("="*70)
    
    for test_name, result in results:
        if result is True:
            status = "[PASS]"
        elif result is False:
            status = "[FAIL]"
        else:
            status = "[SKIP]"
        print(f"{status} {test_name}")
    
    passed = sum(1 for _, r in results if r is True)
    failed = sum(1 for _, r in results if r is False)
    skipped = sum(1 for _, r in results if r is None)
    
    print(f"\nResults: {passed} passed, {failed} failed, {skipped} skipped")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(run_all_tests())
