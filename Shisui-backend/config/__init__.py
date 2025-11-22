"""
Configuration package for Shisui backend
"""

from .model_config import (
    get_openrouter_model,
    get_model_by_alias,
    gemini_flash_model,
    gpt4_model,
    claude_model,
    MODELS
)

__all__ = [
    'get_openrouter_model',
    'get_model_by_alias',
    'gemini_flash_model',
    'gpt4_model',
    'claude_model',
    'MODELS'
]
