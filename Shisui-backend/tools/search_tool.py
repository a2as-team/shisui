import os
import requests
import json
from typing import Dict, Any, List

def search_perplexity(query: str) -> Dict[str, Any]:
    """
    Search the web using Perplexity API.
    
    Args:
        query: The search query string
        
    Returns:
        Dictionary containing the answer and citations
    """
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        return {"answer": "Error: PERPLEXITY_API_KEY not found in environment variables.", "citations": []}

    url = "https://api.perplexity.ai/chat/completions"
    
    payload = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful research assistant. Provide accurate, up-to-date information with citations."
            },
            {
                "role": "user",
                "content": query
            }
        ],
        "temperature": 0.2,
        "top_p": 0.9,
        "return_citations": True,
        "search_domain_filter": ["perplexity.ai"],
        "return_images": False,
        "return_related_questions": False,
        "search_recency_filter": "month",
        "top_k": 0,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 1
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        content = data["choices"][0]["message"]["content"]
        citations = data.get("citations", [])
        
        return {
            "answer": content,
            "citations": citations
        }
    except Exception as e:
        return {
            "answer": f"Error performing search: {str(e)}",
            "citations": []
        }

def get_search_tool():
    """Returns the search tool for agent use"""
    # This is a helper to be consistent with the example pattern
    return search_perplexity
