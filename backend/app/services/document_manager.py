import json
import os
from pathlib import Path
from fastapi import HTTPException
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

PERSIST_DIR = Path("../data/vector_store").resolve()
COLLECTION_NAME = "askdoc"
INDEX_PATH = Path("../data/document_index.json").resolve()

UPLOAD_DIR = Path("../data/documents")
PARSED_DIR = Path("../data/parsed_text")

def load_document_index(index_path: Path):
    if not INDEX_PATH.exists():
        return {}
    return json.loads(INDEX_PATH.read_text())

def save_document_index(index: dict):
    INDEX_PATH.write_text(json.dumps(index, indent=2), encoding='utf-8')
    
def delete_document_by_id(doc_id: str):
    import pdb
    pdb.set_trace()
    index = load_document_index(INDEX_PATH)
    if doc_id not in index:
        raise HTTPException(
            status_code=404,
            detail=f"Document with ID `{doc_id}` not found."
        )
    
    # delete uploaded file
    delete_uploaded_file_for_doc(doc_id, index)
    
    # delete parsed text
    delete_parsed_text_file_for_doc(doc_id, index)

    # delete vectors
    delete_vectors_for_doc(doc_id)

    # remove from index
    del index[doc_id]
    save_document_index(index)
    return {"message": f"Document `{doc_id}`, its parsed text and associated vectors removed."}

def delete_uploaded_file_for_doc(doc_id: str, index):
    file_path = UPLOAD_DIR / index[doc_id]["filename"]
    if file_path.exists():
        try:
            os.remove(file_path)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to delete file {file_path}: {str(e)}"
            ) from e
        
def delete_parsed_text_file_for_doc(doc_id: str, index):
    file_path = UPLOAD_DIR / index[doc_id]["filename"]
    parsed_text_path = PARSED_DIR / (file_path.stem + ".txt")
    if parsed_text_path.exists():
        try:
            os.remove(parsed_text_path)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to delete parsed text {parsed_text_path}: {str(e)}"
            )
        
def delete_vectors_for_doc(doc_id: str):
    try:
        import pdb
        pdb.set_trace()
        import chromadb
        client = chromadb.PersistentClient(path=str(PERSIST_DIR))
        collection = client.get_or_create_collection(name=COLLECTION_NAME)
        collection.delete(where={"doc_id": doc_id})
        # import pdb
        # pdb.set_trace()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete vectors for document {doc_id}: {str(e)}"
        )

def delete_all_total_documents():
    try:
        # 1. Delete all uploaded files
        if UPLOAD_DIR.exists():
            for file in UPLOAD_DIR.glob("*"):
                file.unlink()

        # 2. Delete all parsed text files
        if PARSED_DIR.exists():
            for file in PARSED_DIR.glob("*.txt"):
                file.unlink()

        # 3. Delete all vectors from vector store
        import chromadb
        chroma_client = chromadb.PersistentClient(path=str(PERSIST_DIR))
        collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)
        # import pdb
        # pdb.set_trace()

        all_ids = collection.get()["ids"]
        if all_ids:
            collection.delete(ids=all_ids)


        # 4. Delete document index file
        if INDEX_PATH.exists():
            INDEX_PATH.unlink()

        return {"message": "All documents, parsed text, vectors, and index entries deleted successfully."}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete all documents: {str(e)}"
        )