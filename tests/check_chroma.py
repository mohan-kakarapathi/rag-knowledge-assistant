from backend.app.services.vector_service import collection

print("Collection name:", collection.name)
print("Total chunks:", collection.count())

results = collection.get(
    include=["documents", "metadatas"]
)

print(results)