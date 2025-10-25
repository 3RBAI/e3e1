from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from .models import ChatRequest, UploadResponse
from .views import handle_chat_request, handle_upload_request

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Chat completion endpoint with streaming support
    
    Args:
        request: ChatRequest with messages, model, and optional tools
    
    Returns:
        StreamingResponse with chat completion
    """
    return await handle_chat_request(request)

@router.post("/upload", response_model=UploadResponse)
async def upload_endpoint(file: UploadFile = File(...)):
    """
    File upload endpoint
    
    Args:
        file: Uploaded file
    
    Returns:
        UploadResponse with file URL and metadata
    """
    try:
        # Read file data
        file_data = await file.read()
        
        # Handle upload
        return await handle_upload_request(
            file_data=file_data,
            filename=file.filename,
            size=len(file_data),
            file_type=file.content_type
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "chat"}
