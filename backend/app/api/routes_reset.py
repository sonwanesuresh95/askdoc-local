from fastapi import APIRouter
from pathlib import Path
import shutil
import os

router = APIRouter()

BASE_DIR = Path("../data").resolve()
DOCUMENTS_DIR = BASE_DIR / "documents"
PARSED_DIR = BASE_DIR / "parsed_text"
VECTOR_STORE_DIR = BASE_DIR / "vector_store"
INDEX_FILE = BASE_DIR / "document_index.json"

@router.post("/reset/", summary="Delete all uploaded data and reset vector store")
def reset_all_data():
    try:
        # Delete directories
        for path in [DOCUMENTS_DIR, PARSED_DIR, VECTOR_STORE_DIR]:
            if path.exists():
                shutil.rmtree(path)

        # Delete index file
        if INDEX_FILE.exists():
            os.remove(INDEX_FILE)

        # Re-create folders
        DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
        PARSED_DIR.mkdir(parents=True, exist_ok=True)
        VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

        return {"message": "System reset successful. All documents, parsed text, vectors, and index cleared."}

    except Exception as e:
        return {"error": f"Failed to reset system: {str(e)}"}
