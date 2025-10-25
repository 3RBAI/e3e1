"""
View functions for chat endpoints
Split into sections: All, Requests, Responses
"""
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from typing import Dict, Any
from .models import ChatRequest, UploadRequest, ChatResponse, UploadResponse, ErrorResponse
from .services import ChatService, UploadService
from .utils import sanitize_message, validate_model_id, build_error_response

# All services initialization
chat_service = ChatService()
upload_service = UploadService()

# Requests handlers

async def handle_chat_request(request: ChatRequest) -> StreamingResponse:
    """
    Handle chat completion request with streaming
    """
    try:
        # Validate model
        if not validate_model_id(request.model):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid model ID: {request.model}"
            )
        
        # Sanitize messages
        for message in request.messages:
            message.content = sanitize_message(message.content)
        
        # Stream chat completion
        return StreamingResponse(
            chat_service.stream_chat(
                messages=request.messages,
                model=request.model,
                tools=request.tools,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            ),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        error_response = build_error_response(
            error="Failed to process chat request",
            detail=str(e),
            status_code=500
        )
        raise HTTPException(status_code=500, detail=error_response)

async def handle_upload_request(file_data: bytes, filename: str, size: int, file_type: str) -> UploadResponse:
    """
    Handle file upload request
    """
    try:
        # Validate file
        is_valid, message = upload_service.validate_file(filename, size, file_type)
        if not is_valid:
            raise HTTPException(status_code=400, detail=message)
        
        # Upload file
        file_url = await upload_service.upload_file(file_data, filename, file_type)
        
        return UploadResponse(
            url=file_url,
            filename=filename,
            size=size,
            type=file_type
        )
    
    except HTTPException:
        raise
    except Exception as e:
        error_response = build_error_response(
            error="Failed to upload file",
            detail=str(e),
            status_code=500
        )
        raise HTTPException(status_code=500, detail=error_response)

# Responses helpers

def create_success_response(data: Any, message: str = "Success") -> Dict[str, Any]:
    """Create standardized success response"""
    return {
        "success": True,
        "message": message,
        "data": data
    }

def create_error_response(error: str, detail: str = None) -> ErrorResponse:
    """Create standardized error response"""
    return ErrorResponse(
        error=error,
        detail=detail,
        status_code=500
    )
