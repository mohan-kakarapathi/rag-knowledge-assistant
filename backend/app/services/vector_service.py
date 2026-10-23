
from pathlib import Path
import chromadb
from backend.app.config import (
    CHROMA_DB_PATH,
    CHROMA_COLLECTION_NAME,
)

client = chromadb.PersistentClient(path=str(CHROMA_DB_PATH))

collection = client.get_or_create_collection(
    name=CHROMA_COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"},
)


def store_chunks(
    chunks: list[str],
    embeddings: list[list[float]],
    document_id: str = "employee_handbook",
    source: str = "employee_handbook.txt",
) -> None:
    if len(chunks) != len(embeddings):
        raise ValueError("Each chunk must have one embedding")

    if not chunks:
        raise ValueError("No chunks to store")

    ids = [
        f"{document_id}-{i}"
        for i in range(len(chunks))
    ]

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=[
            {
                "document_id": document_id,
                "chunk_index": i,
                "source": source,
            }
            for i in range(len(chunks))
        ],
    )


def search_chunks(
    query_embedding: list[float],
    n_results: int = 3,
    document_ids: list[str] | None = None,
) -> list[dict]:
    # 1. Validate the query embedding.
    if not query_embedding:
        return []

    # 2. Check whether ChromaDB contains any chunks.
    total_chunks = collection.count()

    if total_chunks == 0:
        return []

    # 3. If an empty document list is explicitly provided,
    # return no results.
    if document_ids is not None and not document_ids:
        return []

    # 4. Prepare the ChromaDB search arguments.
    query_args = {
        "query_embeddings": [query_embedding],
        "n_results": min(n_results, total_chunks),
        "include": ["documents", "metadatas", "distances"],
    }

    # 5. Add a filter only when document IDs are provided.
    if document_ids is not None:
        query_args["where"] = {
            "document_id": {"$in": document_ids}
        }

    # 6. Search ChromaDB.
    results = collection.query(**query_args)

    # 7. Extract the matching chunks and metadata.
    documents = results["documents"][0] or []
    metadatas = results["metadatas"][0] or []
    distances = results["distances"][0] or []

    # 8. Return results in a convenient format.
    return [
        {
            "text": document,
            "metadata": metadata,
            "distance": distance,
        }
        for document, metadata, distance in zip(
            documents, metadatas, distances
        )
    ]


def get_document_ids_by_source(source: str)-> set[str]:
    """Find document IDs associated with a filename."""

    results = collection.get(
        where={"source": source},
        include=["metadatas"]
    )

    metadatas = results.get('metadatas') or []

    return {
        metadata["document_id"]
        for metadata in metadatas
        if metadata and "document_id" in metadata
    }



def delete_document_chunks(document_id: str) -> None:
    """Delete all chunks belonging to a document ID."""
    collection.delete(
        where={"document_id": document_id}
    )


