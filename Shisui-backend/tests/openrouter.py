"""
Test script for OpenRouter API integration
"""
import sys
import os

# Add parent directory to path to import services
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.openrouter_service import OpenRouterService, ask_openrouter


def test_basic_chat():
    """Test basic chat completion"""
    print("Testing OpenRouter API - Basic Chat\n")
    
    try:
        service = OpenRouterService()
        
        messages = [
            {
                "role": "user",
                "content": "What is the meaning of life? Answer in one sentence."
            }
        ]
        
        print(f"Sending request to model: google/gemini-2.5-flash")
        response = service.chat_completion(
            messages=messages,
            model="google/gemini-2.5-flash",
            temperature=0.7
        )
        
        print("\n[SUCCESS] Response received:")
        print(f"Model: {response['model']}")
        print(f"Answer: {response['choices'][0]['message']['content']}")
        print(f"\nTokens used: {response['usage']['total_tokens']}")
        
    except Exception as e:
        print(f"\n[ERROR] Error: {str(e)}")


def test_convenience_function():
    """Test the convenience ask_openrouter function"""
    print("\n" + "="*60)
    print("Testing Convenience Function\n")
    
    try:
        response = ask_openrouter(
            question="Explain quantum computing in one sentence.",
            model="google/gemini-2.5-flash",
            system_prompt="You are a helpful assistant that explains complex topics simply."
        )
        
        print("[SUCCESS] Response:")
        print(response)
        
    except Exception as e:
        print(f"[ERROR] Error: {str(e)}")


def test_different_model():
    """Test with a different model (Gemini)"""
    print("\n" + "="*60)
    print("Testing Different Model (Gemini Flash 2.5)\n")
    
    try:
        response = ask_openrouter(
            question="What are the three laws of robotics?",
            model="google/gemini-2.5-flash"
        )
        
        print("[SUCCESS] Response:")
        print(response)
        
    except Exception as e:
        print(f"[ERROR] Error: {str(e)}")


if __name__ == "__main__":
    print("="*60)
    print("OpenRouter API Test Suite")
    print("="*60)
    
    # Run tests
    test_basic_chat()
    test_convenience_function()
    test_different_model()
    
    print("\n" + "="*60)
    print("Tests completed!")
    print("="*60)
