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
    vectordb = Chroma.from_texts(
        texts=chunks,
        embedding=embedding,
        persist_directory=str(PERSIST_DIR),
        collection_name="askdoc",
        collection_metadata={"hnsw:space": "cosine"},
        metadatas=[{"source": doc_id}] * len(chunks)
    )

    return len(chunks)
