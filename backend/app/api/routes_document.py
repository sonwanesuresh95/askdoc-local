from fastapi import APIRouter, HTTPException
from pathlib import Path
import json
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from app.services.document_manager import (
    delete_all_total_documents,
    load_document_index,
    delete_document_by_id
)

PERSIST_DIR = Path("../data/vector_store")
COLLECTION_NAME = "askdoc"

router = APIRouter()
INDEX_PATH = Path("../data/document_index.json").resolve()

@router.get("/documents/")
def list_documents():
    return load_document_index(INDEX_PATH)

@router.delete("/documents/{doc_id}/")
def delete_document(doc_id: str):
    return delete_document_by_id(doc_id)

@router.delete("/delete_all_docs/")
def delete_all_documents():
    return delete_all_total_documents()
