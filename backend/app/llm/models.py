"""
Factory function for creating LLM instances.
Simplified version that uses OpenAI client directly.
"""

import os
from openai import AsyncOpenAI


def get_llm_by_name(model_name: str):
    """
    Factory function to create LLM instances from string names.
    
    Args:
        model_name: Model name like 'gpt-4o', 'gpt-4o-mini', etc.
    
    Returns:
        AsyncOpenAI client configured with the model
    
    Raises:
        ValueError: If model_name is not recognized
    """
    if not model_name:
        raise ValueError('Model name cannot be empty')
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError('OPENAI_API_KEY environment variable is required')
    
    return AsyncOpenAI(api_key=api_key)
