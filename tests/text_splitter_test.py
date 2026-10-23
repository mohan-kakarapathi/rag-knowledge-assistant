
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Read the document
file_path = Path("data/employee_handbook.txt")
document_text = file_path.read_text(encoding="utf-8")

# 2. Create the text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
)

# 3. Split the document
chunks = text_splitter.split_text(document_text)

# 4. Print the chunks
for index, chunk in enumerate(chunks, start=1):
    print(f"\nChunk {index}:")
    print(chunk)
    print(f"Characters: {len(chunk)}")
