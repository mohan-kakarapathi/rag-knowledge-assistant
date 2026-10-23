
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

from io import BytesIO
from pypdf import PdfReader


def extract_uploaded_text(filename: str, content: bytes) -> str:
    """Extract text from a supported uploaded file."""

    extension = filename.lower().rsplit(".", 1)[-1]

    if extension == "txt":
        text = content.decode("utf-8-sig")

    elif extension == "pdf":
        reader = PdfReader(BytesIO(content))
        text = "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    else:
        raise ValueError("Only PDF and TXT files are supported.")

    if not text.strip():
        raise ValueError(
            "No readable text found in the document."
        )

    return text


def load_document(file_path: str) -> str:
    """Read a UTF-8 text document and return its content."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Document not found: {path}")

    return path.read_text(encoding="utf-8")


def split_document(
    document_text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> list[str]:
    """Split document text into overlapping chunks."""
    if not document_text.strip():
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    return splitter.split_text(document_text)
    


# result = load_document(
#     r'C:\Users\Ennoventure\Documents\AI-Projects\rag-knowledge-assistant\data\employee_handbook.txt'
# )

# split_document(result, 100, 80)