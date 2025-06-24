from fastapi import APIRouter, File, UploadFile, HTTPException
import shutil
from pathlib import Path
from app.services.document_parser import parse_document
from app.services.embedder import chunk_text, embed_and_store
import json
from datetime import datetime

INDEX_PATH = Path("../data/document_index.json")

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
        # parse document
        parsed_text = parse_document(file_path)
        parsed_path = PARSED_DIR / (file_path.stem + ".txt")
        parsed_path.write_text(parsed_text, encoding="utf-8")

        # embed document
        chunks = chunk_text(parsed_text, chunk_size=1000)
        print(f"[UPLOAD] Parsed {len(parsed_text)} characters")
        print(f"[UPLOAD] Generated {len(chunks)} chunks for `{file.filename}`")

        chunk_count = embed_and_store(chunks, doc_id=file.filename)

        print(f"[UPLOAD] Stored {chunk_count} chunks for `{file.filename}`")


        # save metadata
        save_metadata(doc_id=file.filename, filename=file.filename)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse: {e}")

    return {
        "filename": file.filename, 
        "parsed_chunks": chunk_count,
        "status": "uploaded"
        }

def save_metadata(doc_id: str, filename: str):
    if not INDEX_PATH.exists():
        INDEX_PATH.write_text(json.dumps({}))
    
    index = json.loads(INDEX_PATH.read_text())
    index[doc_id] = {
        "filename": filename,
        "uploaded_at": datetime.now().isoformat()
    }
    INDEX_PATH.write_text(json.dumps(index, indent=4))