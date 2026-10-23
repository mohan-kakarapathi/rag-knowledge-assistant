
from fastapi import APIRouter, HTTPException

from backend.app.models.ask import AskRequest, AskResponse
from backend.app.services.rag_service import answer_question

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    try:
        result = answer_question(
            request.question
        )
        return result
    except Exception:
        # The detailed error remains in the server logs.
        raise HTTPException(
            status_code=500,
            detail="Failed to generate an answer. Please try again.",
        )
