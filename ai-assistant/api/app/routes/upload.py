from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil
import uuid
from pathlib import Path
from app.core.config import get_settings

router = APIRouter()
settings = get_settings()
UPLOAD_DIR = Path(settings.upload_dir)

ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}. Only images are allowed.")

    # Generate unique filename
    extension = Path(file.filename).suffix
    filename = f"{uuid.uuid4()}{extension}"
    file_path = UPLOAD_DIR / filename

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")

    return JSONResponse(content={"url": f"/uploads/{filename}"})
