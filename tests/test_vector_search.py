
from backend.app.services.document_service import (
    load_document,
    split_document,
)
from backend.app.services.embedding_service import embed_texts
from backend.app.services.vector_service import store_chunks


def main():
    document = load_document(
        "data/employee_handbook.txt"
    )

    chunks = split_document(
        document,
        chunk_size=100,
        chunk_overlap=20,
    )

    embeddings = embed_texts(chunks)

    store_chunks(chunks, embeddings)

    print("Chunks stored:", len(chunks))


if __name__ == "__main__":
    main()
