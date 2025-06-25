
# 🧠 AskDoc Local - RAG API with FastAPI + Ollama + LangChain

AskDoc Local is a fully offline, API-first Retrieval-Augmented Generation (RAG) system built using:

- 🧩 **FastAPI** – For REST APIs  
- 💬 **Ollama** – For running lightweight LLMs like `mistral` locally  
- 🔗 **LangChain** – For document chunking, embedding, and querying  
- 📄 **PDF/CSV/XLSX/DOCX** – Multi-format document support  
- 🧠 **Chroma (or replaceable)** – Local vector store (swappable with FAISS or Weaviate)  

---

## 📦 Features

| Feature | Status |
|--------|--------|
| Upload documents (PDF, CSV, XLSX, DOCX) | ✅ |
| Parse and chunk text using LangChain | ✅ |
| Embed using Ollama models (e.g., mistral) | ✅ |
| Store embeddings locally in ChromaDB | ✅ |
| Ask questions via `/query/` API | ✅ |
| Delete single or all documents | ✅ |
| Debug API to inspect indexed documents | ✅ |
| Reset API to wipe everything clean | ✅ |

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/sonwanesuresh95/askdoc-local.git
cd askdoc-local
pip install -r requirements.txt
```

### 2. Start Ollama

```bash
ollama run mistral
```

Make sure Ollama is running and the model is pulled.

### 3. Start the API server

```bash
uvicorn app.main:app --reload
```

---

## 🛠️ API Endpoints

### 📄 Upload Document

```http
POST /upload/
Content-Type: multipart/form-data
```

Upload `.pdf`, `.docx`, `.csv`, or `.xlsx`. The document is parsed, chunked, embedded, and stored.

---

### ❓ Ask a Question

```http
POST /query/
{
  "query": "What is Acme Corp's revenue?"
}
```

Returns an answer based on uploaded and embedded documents.

---

### 🗑️ Delete a Document

```http
DELETE /api/documents/{doc_id}
```

Deletes uploaded file, parsed `.txt`, and embeddings.

---

### 🔄 Reset Entire System

```http
POST /reset/
```

Deletes all uploaded files, parsed text, and vector DB.

---

### 🐞 Debug Vector Store

```http
GET /debug/vectorstore
```

Returns a list of indexed documents and their chunk counts.

---

## 📁 Directory Structure

```
askdoc-local/
├── app/
│   ├── main.py
│   ├── routes/
│   ├── services/
├── data/
│   ├── documents/         # Uploaded files
│   ├── parsed_text/       # Parsed .txt files
│   ├── vector_store/      # Chroma DB data
│   └── document_index.json
```

---

## 🧠 Embedding Model

- Uses `OllamaEmbeddings(model="mistral")` from `langchain_ollama`
- You can replace with any local model supported by Ollama (e.g., `llama2`, `codellama`, `phi`)

---

## 🔄 Future Plans

- [ ] Frontend UI using React + Material UI  
- [ ] Weaviate-based vector backend  
- [ ] Docker + CI/CD setup  
- [ ] Streamlit Playground UI

---

## 🧑‍💻 Author

**Suresh Sonwane**  
GitHub: [@sonwanesuresh95](https://github.com/sonwanesuresh95)

---

## 📜 License

MIT License
