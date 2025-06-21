from fastapi import APIRouter, File, UploadFile, HTTPException
import shutil
from pathlib import Path
from app.services.document_parser import parse_document

router = APIRouter()

UPLOAD_DIR = Path("../data/documents")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
PARSED_DIR = Path("../data/parsed_text")
PARSED_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(("pdf", "docx", "csv", "xlsx")):
        raise HTTPException(status_code=400, detail="unsupported file type")
    
    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        parsed_text = parse_document(file_path)
        parsed_path = PARSED_DIR / (file_path.stem + ".txt")
        parsed_path.write_text(parsed_text, encoding="utf-8")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse: {e}")

    return {"filename": file.filename, "status": "uploaded"}
