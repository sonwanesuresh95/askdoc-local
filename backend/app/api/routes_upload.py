from fastapi import APIRouter, File, UploadFile, HTTPException
import shutil
from pathlib import Path

router = APIRouter()

UPLOAD_DIR = Path("data/documents")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(("pdf", "docx", "csv", "xlsx")):
        raise HTTPException(status_code=400, detail="unsupported file type")
    
    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "status": "uploaded"}
