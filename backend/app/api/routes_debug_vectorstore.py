from fastapi import APIRouter
import chromadb
from collections import Counter
from pathlib import Path

router = APIRouter()

PERSIST_DIR = Path("../data/vector_store").resolve()
COLLECTION_NAME = "askdoc"

@router.get("/debug/vectorstore/")
def debug_vectorstore():
    client = chromadb.PersistentClient(path=str(PERSIST_DIR))
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    results = collection.get(include=["metadatas", "documents"], limit=1000)  # Adjust limit if needed

    all_ids = results.get("ids", [])
    metadatas = results.get("metadatas", [])
    documents = results.get("documents", [])

    # Count how many vectors per doc_id/source
    source_counts = Counter(meta.get("source") for meta in metadatas if "source" in meta)

    return {
        "total_embeddings": len(all_ids),
        "documents_present": list(source_counts.keys()),
        "embedding_count_per_document": dict(source_counts),
        "sample_documents": [
            {
                "id": all_ids[i],
                "source": metadatas[i].get("source"),
                "content": documents[i][:100] + "..." if documents[i] else None
            }
            for i in range(min(5, len(all_ids)))
        ]
    }
