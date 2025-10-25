"""
Utility functions for chat operations
"""
from typing import Dict, Any, List
import re
from datetime import datetime

def sanitize_message(content: str) -> str:
    """Sanitize message content"""
    # Remove potentially harmful content
    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<iframe[^>]*>.*?</iframe>', '', content, flags=re.DOTALL | re.IGNORECASE)
    return content.strip()

def format_timestamp() -> str:
    """Get formatted timestamp"""
    return datetime.utcnow().isoformat() + "Z"

def validate_model_id(model_id: str) -> bool:
    """Validate model ID"""
    valid_models = ["gpt-4o", "gpt-4o-mini", "gpt-5", "gpt-4-turbo"]
    return model_id in valid_models

def extract_tool_parameters(tool_call: Dict[str, Any]) -> Dict[str, Any]:
    """Extract parameters from tool call"""
    try:
        if "function" in tool_call and "arguments" in tool_call["function"]:
            import json
            return json.loads(tool_call["function"]["arguments"])
    except Exception:
        return {}
    return {}

def build_error_response(error: str, detail: str = None, status_code: int = 500) -> Dict[str, Any]:
    """Build standardized error response"""
    response = {
        "error": error,
        "status_code": status_code,
        "timestamp": format_timestamp()
    }
    if detail:
        response["detail"] = detail
    return response

def calculate_token_estimate(text: str) -> int:
    """Rough estimate of token count"""
    # Rough approximation: 1 token ≈ 4 characters
    return len(text) // 4

def truncate_messages(messages: List[Dict[str, Any]], max_tokens: int = 4000) -> List[Dict[str, Any]]:
    """Truncate message history to fit within token limit"""
    total_tokens = sum(calculate_token_estimate(msg.get("content", "")) for msg in messages)
    
    if total_tokens <= max_tokens:
        return messages
    
    # Keep system message and recent messages
    truncated = [messages[0]] if messages and messages[0].get("role") == "system" else []
    
    for msg in reversed(messages[1:]):
        msg_tokens = calculate_token_estimate(msg.get("content", ""))
        if total_tokens - msg_tokens >= 0:
            truncated.insert(1 if truncated else 0, msg)
            total_tokens -= msg_tokens
        else:
            break
    
    return truncated
