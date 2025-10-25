import os
from typing import List, Dict, Any, AsyncGenerator
from openai import AsyncOpenAI
from .models import Message, ToolDefinition, ChatResponse, ToolCall
from .prompts import get_system_prompt, get_tool_prompt, ERROR_MESSAGES
import json

class ChatService:
    """Service for handling chat operations"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def _build_tool_definitions(self, tools: List[ToolDefinition]) -> List[Dict[str, Any]]:
        """Build OpenAI tool definitions from ChatKit tools"""
        tool_defs = []
        
        for tool in tools:
            if tool.id == "search_docs":
                tool_defs.append({
                    "type": "function",
                    "function": {
                        "name": "search_docs",
                        "description": "Search through documentation",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "The search query"
                                }
                            },
                            "required": ["query"]
                        }
                    }
                })
            elif tool.id == "web_search":
                tool_defs.append({
                    "type": "function",
                    "function": {
                        "name": "web_search",
                        "description": "Search the web",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "The search query"
                                }
                            },
                            "required": ["query"]
                        }
                    }
                })
        
        return tool_defs
    
    async def stream_chat(
        self,
        messages: List[Message],
        model: str,
        tools: List[ToolDefinition] = None,
        temperature: float = 0.7,
        max_tokens: int = None
    ) -> AsyncGenerator[str, None]:
        """Stream chat completion from OpenAI"""
        try:
            # Add system prompt
            system_prompt = get_system_prompt(model)
            formatted_messages = [
                {"role": "system", "content": system_prompt}
            ]
            formatted_messages.extend([msg.model_dump() for msg in messages])
            
            # Build tool definitions
            tool_definitions = None
            if tools:
                tool_definitions = self._build_tool_definitions(tools)
            
            # Create streaming completion
            stream = await self.client.chat.completions.create(
                model=model,
                messages=formatted_messages,
                tools=tool_definitions if tool_definitions else None,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            # Stream responses
            async for chunk in stream:
                delta = chunk.choices[0].delta
                
                if delta.content:
                    yield f"data: {json.dumps({'content': delta.content})}\n\n"
                
                if delta.tool_calls:
                    tool_calls_data = [
                        {
                            "id": tc.id,
                            "type": tc.type,
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in delta.tool_calls
                    ]
                    yield f"data: {json.dumps({'tool_calls': tool_calls_data})}\n\n"
            
            yield "data: [DONE]\n\n"
            
        except Exception as e:
            error_msg = ERROR_MESSAGES.get("api_error", str(e))
            yield f"data: {json.dumps({'error': error_msg})}\n\n"

class UploadService:
    """Service for handling file uploads"""
    
    def __init__(self):
        self.max_size = 10485760  # 10MB
        self.allowed_types = [
            "image/jpeg", "image/png", "image/gif", "image/webp",
            "application/pdf", "text/plain", "text/csv",
            "application/json", "application/xml"
        ]
    
    def validate_file(self, filename: str, size: int, file_type: str) -> tuple[bool, str]:
        """Validate uploaded file"""
        if size > self.max_size:
            return False, ERROR_MESSAGES["file_too_large"]
        
        if file_type not in self.allowed_types:
            return False, ERROR_MESSAGES["unsupported_file"]
        
        return True, "File is valid"
    
    async def upload_file(self, file_data: bytes, filename: str, file_type: str) -> str:
        """Upload file to storage (placeholder - implement with your storage solution)"""
        # TODO: Implement actual file upload to Vercel Blob or other storage
        # For now, return a placeholder URL
        return f"https://storage.example.com/{filename}"
