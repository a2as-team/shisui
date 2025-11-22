"""
Test all agent tools: Search, Timer, and Exam
"""
import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.search_tool import search_perplexity
from tools.timer_tool import start_timer
from tools.exam_tool import generate_test, evaluate_answer


def test_timer_tool():
    """Test the timer tool"""
    print("\n" + "="*60)
    print("Test 1: Timer Tool")
    print("="*60)
    
    try:
        # Test starting a timer
        print("\n[INFO] Starting a 25-minute Pomodoro timer...")
        result = start_timer(25, "Pomodoro Study Session")
        
        print(f"\n[SUCCESS] Timer started!")
        print(f"  Action: {result['action']}")
        print(f"  Duration: {result['duration_minutes']} minutes")
        print(f"  Label: {result['label']}")
        print(f"  Message: {result['message']}")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Timer tool failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_search_tool():
    """Test the search tool with Perplexity API"""
    print("\n" + "="*60)
    print("Test 2: Search Tool (Perplexity)")
    print("="*60)
    
    try:
        # Check if API key exists
        api_key = os.getenv("PERPLEXITY_API_KEY")
        if not api_key:
            print("\n[SKIP] PERPLEXITY_API_KEY not found in .env")
            print("  Add your Perplexity API key to test this feature")
            return None
        
        # Test search
        print("\n[INFO] Searching: 'What is quantum computing?'")
        result = search_perplexity("What is quantum computing in simple terms?")
        
        if "error" in result.get("answer", "").lower():
            print(f"\n[ERROR] Search failed: {result['answer']}")
            return False
        
        print(f"\n[SUCCESS] Search completed!")
        print(f"\nAnswer (first 200 chars):")
        print(f"  {result['answer'][:200]}...")
        
        if result.get('citations'):
            print(f"\nCitations: {len(result['citations'])} found")
            for idx, citation in enumerate(result['citations'][:3], 1):
                print(f"  {idx}. {citation}")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Search tool failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_exam_tool():
    """Test the exam generation tool"""
    print("\n" + "="*60)
    print("Test 3: Exam Tool")
    print("="*60)
    
    try:
        # Check if API key exists
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("\n[SKIP] OPENROUTER_API_KEY not found in .env")
            print("  Add your OpenRouter API key to test this feature")
            return None
        
        # Test exam generation
        print("\n[INFO] Generating a 3-question test on 'Python Basics'...")
        result = generate_test("Python Basics", difficulty="easy", num_questions=3)
        
        if "error" in result:
            print(f"\n[ERROR] Exam generation failed: {result['error']}")
            return False
        
        print(f"\n[SUCCESS] Exam generated!")
        print(f"  Title: {result.get('title', 'N/A')}")
        print(f"  Questions: {len(result.get('questions', []))}")
        
        if result.get('pdf_url'):
            print(f"  PDF URL: {result['pdf_url']}")
        
        # Display first question
        if result.get('questions'):
            q1 = result['questions'][0]
            print(f"\n  Sample Question:")
            print(f"    {q1['question']}")
            for opt in q1.get('options', [])[:2]:
                print(f"      {opt}")
            print(f"    ...")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Exam tool failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_eval_tool():
    """Test the answer evaluation tool"""
    print("\n" + "="*60)
    print("Test 4: Answer Evaluation Tool")
    print("="*60)
    
    try:
        # Check if API key exists
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("\n[SKIP] OPENROUTER_API_KEY not found in .env")
            return None
        
        # Test evaluation
        question = "What is 2 + 2?"
        correct_answer = "4"
        user_answer = "4"
        
        print(f"\n[INFO] Evaluating answer...")
        print(f"  Question: {question}")
        print(f"  User Answer: {user_answer}")
        print(f"  Correct Answer: {correct_answer}")
        
        result = evaluate_answer(question, user_answer, correct_answer)
        
        if "error" in result:
            print(f"\n[ERROR] Evaluation failed: {result['error']}")
            return False
        
        print(f"\n[SUCCESS] Evaluation completed!")
        print(f"  Correct: {result.get('correct', False)}")
        print(f"  Feedback: {result.get('feedback', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Eval tool failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tool tests"""
    print("\n" + "="*70)
    print(" Agent Tools Test Suite")
    print("="*70)
    
    results = []
    
    # Run tests
    results.append(("Timer Tool", test_timer_tool()))
    results.append(("Search Tool", test_search_tool()))
    results.append(("Exam Generation", test_exam_tool()))
    results.append(("Answer Evaluation", test_eval_tool()))
    
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
    
    if skipped > 0:
        print("\nNote: Add API keys to .env to enable skipped tests:")
        print("  - PERPLEXITY_API_KEY for search")
        print("  - OPENROUTER_API_KEY for exam generation")
    
    print("="*70)


if __name__ == "__main__":
    run_all_tests()
