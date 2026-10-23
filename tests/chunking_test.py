from pathlib import Path

file_path = Path('data/employee_handbook.txt')

with open(file_path, 'r', encoding='utf-8') as file:
    document_data = file.read()

print(f'+++++++++++++++++++++: {document_data}')

chunks = [
    paragraph.strip()
    for paragraph in document_data.split('\n\n')
    if paragraph.strip()
]


print(chunks)


for index, chunk in enumerate(chunks, start=1):
    print(f"\nChunk {index}:")
    print(chunk)