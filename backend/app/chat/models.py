from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal

# All Models

class Message(BaseModel):
    """Chat message model"""
    role: Literal["user", "assistant", "system"]
    content: str
    name: Optional[str] = None

class ToolDefinition(BaseModel):
    """Tool definition model"""
    id: str
    label: str
    shortLabel: Optional[str] = None
    icon: Optional[str] = None
    pinned: Optional[bool] = False

class ToolCall(BaseModel):
    """Tool call model"""
    id: str
    type: str = "function"
    function: Dict[str, Any]

# Requests

class ChatRequest(BaseModel):
    """Chat request model"""
    messages: List[Message]
    model: str = Field(default="gpt-4o", description="Model to use for chat")
    tools: Optional[List[ToolDefinition]] = None
    temperature: Optional[float] = Field(default=0.7, ge=0, le=2)
    max_tokens: Optional[int] = Field(default=None, ge=1)
    stream: bool = Field(default=True, description="Enable streaming response")

class UploadRequest(BaseModel):
    """File upload metadata"""
    filename: str
    size: int
    type: str

# Responses

class ChatResponse(BaseModel):
    """Chat response model"""
    content: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None
    finish_reason: Optional[str] = None

class UploadResponse(BaseModel):
    """File upload response"""
    url: str
    filename: str
    size: int
    type: str
    message: str = "File uploaded successfully"

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    status_code: int
