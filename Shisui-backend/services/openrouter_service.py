import os
import requests
import json
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class OpenRouterService:
    """Service for interacting with OpenRouter API"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.site_url = os.getenv("SITE_URL", "http://localhost:8000")
        self.site_name = os.getenv("SITE_NAME", "Shisui Learning Assistant")
        
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "google/gemini-2.5-flash",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> Dict:
        """
        Send a chat completion request to OpenRouter
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model identifier (e.g., "google/gemini-2.5-flash", "openai/gpt-4o", "anthropic/claude-3-opus")
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response
            
        Returns:
            Response dictionary from OpenRouter API
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": self.site_url,
            "X-Title": self.site_name,
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
            
        if stream:
            payload["stream"] = True
        
        try:
            response = requests.post(
                url=self.base_url,
                headers=headers,
                data=json.dumps(payload),
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"OpenRouter API request failed: {str(e)}")
    
    def get_available_models(self) -> Dict:
        """
        Get list of available models from OpenRouter
        
        Returns:
            Dictionary containing available models
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        
        try:
            response = requests.get(
                url="https://openrouter.ai/api/v1/models",
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch models: {str(e)}")


# Convenience function for quick usage
def ask_openrouter(
    question: str,
    model: str = "google/gemini-2.5-flash",
    system_prompt: Optional[str] = None
) -> str:
    """
    Quick helper function to ask a question to OpenRouter
    
    Args:
        question: The user's question
        model: Model to use
        system_prompt: Optional system prompt
        
    Returns:
        The assistant's response text
    """
    service = OpenRouterService()
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": question})
    
    response = service.chat_completion(messages=messages, model=model)
    return response["choices"][0]["message"]["content"]
