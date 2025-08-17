from fastapi import APIRouter, HTTPException
from uuid import uuid4
from datetime import datetime
from pydantic import BaseModel

router = APIRouter(tags=["uploads"])

# Define request model
class InitUploadRequest(BaseModel):
    name: str
    size: int
    contentType: str

# Define response model (optional but clean)
class InitUploadResponse(BaseModel):
    uploadId: str
    name: str
    size: int
    contentType: str
    createdAt: str


@router.post("/init", response_model=InitUploadResponse)
async def init_upload(payload: InitUploadRequest):
    """
    Initialize an upload session.
    Expects JSON body like:
    {
        "name": "myfile.txt",
        "size": 12345,
        "contentType": "text/plain"
    }
    """

    # Validate size (optional rule)
    if payload.size <= 0:
        raise HTTPException(status_code=400, detail="File size must be greater than zero")

    # Generate upload ID
    upload_id = str(uuid4())

    # Return response
    return InitUploadResponse(
        uploadId=upload_id,
        name=payload.name,
        size=payload.size,
        contentType=payload.contentType,
        createdAt=datetime.utcnow().isoformat()
    )
