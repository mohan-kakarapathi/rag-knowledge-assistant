
from uuid import uuid4

from backend.app.services.document_service import (
    extract_uploaded_text,
    split_document,
)
from backend.app.services.embedding_service import embed_texts
from backend.app.services.vector_service import (
    store_chunks,
    get_document_ids_by_source,
    delete_document_chunks
)

from backend.app.config import CHUNK_SIZE, CHUNK_OVERLAP



def ingest_document(filename: str, content: bytes) -> dict:
    """Process an uploaded document and store its chunks."""

    text = extract_uploaded_text(filename, content)

    chunks = split_document(
        text,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    if not chunks:
        raise ValueError("The document did not produce any chunks.")

    embeddings = embed_texts(chunks)


    # Find existing documents with the same filename
    old_document_ids = get_document_ids_by_source(filename)


    # A new ID prevents one upload from overwriting another.
    document_id = uuid4().hex

    store_chunks(
        chunks=chunks,
        embeddings=embeddings,
        document_id=document_id,
        source=filename,
    )

    # Delete old chunks after the new document is stored
    for old_id in old_document_ids:
        delete_document_chunks(old_id)


    return {
        "document_id": document_id,
        "filename": filename,
        "chunks_count": len(chunks),
    }
