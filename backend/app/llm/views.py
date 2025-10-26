"""
Response models for LLM invocations.
"""

from typing import Generic, TypeVar, Union

from pydantic import BaseModel

T = TypeVar('T', bound=Union[BaseModel, str])


class ChatInvokeUsage(BaseModel):
    """Usage information for a chat model invocation."""

    prompt_tokens: int
    prompt_cached_tokens: int | None = None
    prompt_cache_creation_tokens: int | None = None
    prompt_image_tokens: int | None = None
    completion_tokens: int
    total_tokens: int


class ChatInvokeCompletion(BaseModel, Generic[T]):
    """Response from a chat model invocation."""

    completion: T
    thinking: str | None = None
    redacted_thinking: str | None = None
    usage: ChatInvokeUsage | None = None
    stop_reason: str | None = None
