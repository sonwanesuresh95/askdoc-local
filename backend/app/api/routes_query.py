from fastapi import APIRouter, Query
from pydantic import BaseModel
from app.services.qa_engine import answer_question

router = APIRouter()

class QuestionRequest(BaseModel):
    query: str

@router.post("/query/")
async def query_ask(request: QuestionRequest):
    try:
        answer = answer_question(request.query)
        return {"query": request.query, "answer": answer}
    except Exception as e:
        return {"error": str(e)}
