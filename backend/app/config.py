import os
from pathlib import Path

from dotenv import load_dotenv

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Load .env from the project root
load_dotenv(PROJECT_ROOT / ".env")

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from the .env file")

# Models
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL", "gemini-embedding-001"
)
GENERATION_MODEL = os.getenv(
    "GENERATION_MODEL", "gemini-3.5-flash-lite"
)
EMBEDDING_DIMENSIONS = int(
    os.getenv("EMBEDDING_DIMENSIONS", "768")
)

# Document processing
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024

# Retrieval
TOP_K = int(os.getenv("TOP_K", "3"))

# ChromaDB
CHROMA_DB_PATH = PROJECT_ROOT / os.getenv(
    "CHROMA_DB_PATH", "data/chroma_db"
)
CHROMA_COLLECTION_NAME = os.getenv(
    "CHROMA_COLLECTION_NAME", "employee_handbook"
)

# Generation settings
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0"))