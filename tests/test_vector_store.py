
from backend.app.services.document_service import (
    load_document,
    split_document,
)
from backend.app.services.embedding_service import (
    embed_texts,
    embed_query,
)
from backend.app.services.vector_service import (
    store_chunks,
    search_chunks,
)


def main():
    # 1. Load the handbook
    document = load_document("data/employee_handbook.txt")

    # 2. Split it into chunks
    chunks = split_document(
        document,
        chunk_size=100,
        chunk_overlap=20,
    )

    print("Chunks created:", len(chunks))

    # 3. Generate document embeddings
    embeddings = embed_texts(chunks)

    # 4. Store chunks and embeddings in ChromaDB
    store_chunks(chunks, embeddings)

    print("Chunks stored in ChromaDB")

    # 5. Convert the question into an embedding
    question = "How many vacation days can I take?"
    query_vector = embed_query(question)

    # 6. Search ChromaDB
    results = search_chunks(query_vector, n_results=3)

    print("\nQuestion:", question)
    print("\nRetrieved results:")

    for result in results:
        print("\nText:", result["text"])
        print("Distance:", round(result["distance"], 4))
        print("Metadata:", result["metadata"])


if __name__ == "__main__":
    main()
