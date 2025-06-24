from fastapi import APIRouter, HTTPException
from pathlib import Path
import json

router = APIRouter()
INDEX_PATH = Path("../data/document_index.json").resolve()

@router.get("/documents/")
def list_documents():
    if not INDEX_PATH.exists():
        return {}
    return json.loads(INDEX_PATH.read_text(encoding='utf-8'))

@router.delete("/documents/{doc_id}/")
def delete_document(doc_id: str):
    if not INDEX_PATH.exists():
        raise HTTPException(status_code=404, detail="Document index not found")
    
    index = json.loads(INDEX_PATH.read_text(encoding='utf-8'))
    
    if doc_id not in index:
        raise HTTPException(status_code=404, detail="Document not found")
    
    del index[doc_id]
    INDEX_PATH.write_text(json.dumps(index, indent=2), encoding='utf-8')
    
    return {"message": f"Document `{doc_id}` deleted successfully"}