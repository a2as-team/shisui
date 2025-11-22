"""
Model configuration for ADK agents using LiteLLM with OpenRouter
"""
import os
from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm

# Load environment variables
load_dotenv()

# Get API key from environment
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in environment variables")

# Default model configuration
DEFAULT_MODEL = "openrouter/google/gemini-2.5-flash"

def get_openrouter_model(model_name: str = DEFAULT_MODEL) -> LiteLlm:
    """
    Get a LiteLLM model instance configured for OpenRouter
    
    Args:
        model_name: OpenRouter model identifier (format: openrouter/provider/model-name)
        
    Returns:
        LiteLlm instance configured with the specified model
    """
    return LiteLlm(
        model=model_name,
        api_key=OPENROUTER_API_KEY
    )

# Pre-configured model instances for common use cases
gemini_flash_model = get_openrouter_model("openrouter/google/gemini-2.5-flash")
gpt4_model = get_openrouter_model("openrouter/openai/gpt-4o")
claude_model = get_openrouter_model("openrouter/anthropic/claude-3-sonnet")

# Model aliases for easy switching
MODELS = {
    "gemini-flash": "openrouter/google/gemini-2.5-flash",
    "gemini-pro": "openrouter/google/gemini-pro-1.5",
    "gpt-4": "openrouter/openai/gpt-4o",
    "gpt-4-turbo": "openrouter/openai/gpt-4-turbo",
    "claude-opus": "openrouter/anthropic/claude-3-opus",
    "claude-sonnet": "openrouter/anthropic/claude-3-sonnet",
    "llama-70b": "openrouter/meta-llama/llama-3.1-70b-instruct",
}

def get_model_by_alias(alias: str) -> LiteLlm:
    """
    Get a model by its alias
    
    Args:
        alias: Model alias (e.g., "gemini-flash", "gpt-4")
        
    Returns:
        LiteLlm instance
    """
    if alias not in MODELS:
        raise ValueError(f"Unknown model alias: {alias}. Available: {list(MODELS.keys())}")
    
    return get_openrouter_model(MODELS[alias])
