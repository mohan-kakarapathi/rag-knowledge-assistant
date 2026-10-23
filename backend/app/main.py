
from fastapi import FastAPI

from backend.app.routes.ask import router as ask_router
from backend.app.routes.documents import router as documents_router

app = FastAPI(
    title="RAG Knowledge Assistant",
    description="Upload documents and ask questions about their content.",
    version="1.0.0",
)

app.include_router(ask_router)
app.include_router(documents_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
