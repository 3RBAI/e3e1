"""
LLM module for managing different language models.

Usage:
    from app.llm import ChatOpenAI, UserMessage, SystemMessage
    
    model = ChatOpenAI(model="gpt-4o", api_key="...")
    messages = [
        SystemMessage(content="You are a helpful assistant"),
        UserMessage(content="Hello!")
    ]
    response = await model.ainvoke(messages)
"""

from typing import TYPE_CHECKING

# Lightweight imports that are commonly used
from app.llm.base import BaseChatModel
from app.llm.messages import (
    AssistantMessage,
    BaseMessage,
    SystemMessage,
    UserMessage,
)
from app.llm.messages import ContentPartImageParam as ContentImage
from app.llm.messages import ContentPartRefusalParam as ContentRefusal
from app.llm.messages import ContentPartTextParam as ContentText
from app.llm.exceptions import ModelError, ModelProviderError, ModelRateLimitError
from app.llm.views import ChatInvokeCompletion, ChatInvokeUsage
from app.llm.schema import SchemaOptimizer

# Type stubs for lazy imports
if TYPE_CHECKING:
    from app.llm.models import get_llm_by_name

__all__ = [
    # Message types
    'BaseMessage',
    'UserMessage',
    'SystemMessage',
    'AssistantMessage',
    # Content parts
    'ContentText',
    'ContentRefusal',
    'ContentImage',
    # Base model
    'BaseChatModel',
    # Views
    'ChatInvokeCompletion',
    'ChatInvokeUsage',
    # Exceptions
    'ModelError',
    'ModelProviderError',
    'ModelRateLimitError',
    # Schema optimizer
    'SchemaOptimizer',
    # Factory function
    'get_llm_by_name',
]


def __getattr__(name: str):
    """Lazy import mechanism for get_llm_by_name."""
    if name == 'get_llm_by_name':
        from app.llm.models import get_llm_by_name
        return get_llm_by_name
    
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
