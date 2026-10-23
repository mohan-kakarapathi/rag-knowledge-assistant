
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from backend.app.config import (
    GEMINI_API_KEY,
    EMBEDDING_MODEL,
    EMBEDDING_DIMENSIONS,
)

embeddings = GoogleGenerativeAIEmbeddings(
    model=EMBEDDING_MODEL,
    google_api_key=GEMINI_API_KEY,
    output_dimensionality=EMBEDDING_DIMENSIONS,
)


def embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []

    return embeddings.embed_documents(texts)


def embed_query(query: str) -> list[float]:
    if not query.strip():
        raise ValueError("Query cannot be empty")

    return embeddings.embed_query(query)
