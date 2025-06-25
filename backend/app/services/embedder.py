from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

from pathlib import Path

PERSIST_DIR = Path("../data/vector_store").resolve()

# step 1: Chunk the text
def chunk_text(text: str, chunk_size: int = 512, chunk_overlap: int = 64) -> list[str]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    return text_splitter.split_text(text)

def embed_and_store(chunks: list[str], doc_id: str):
    embedding = OllamaEmbeddings(model="mistral")  # uses ollama backend
    vectordb = Chroma(
        embedding_function=embedding,
        persist_directory=str(PERSIST_DIR),
        collection_name="askdoc",
        collection_metadata={"hnsw:space": "cosine"},
        )

    # Filter out empty or invalid chunks
    clean_chunks = [c for c in chunks if c and isinstance(c, str) and c.strip()]

    if not clean_chunks:
        raise ValueError(f"No valid text chunks found for document `{doc_id}`")

    vectordb.add_texts(
        texts=clean_chunks,
        metadatas=[{"source": doc_id}] * len(clean_chunks)
        )
    
    vectordb.persist()
    print(f"[EMBED] Persisted vector store with {len(clean_chunks)} chunks for {doc_id}")

    return len(chunks)
