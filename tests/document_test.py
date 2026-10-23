from pathlib import Path

#locate the document
file_path = Path('data/employee_handbook.txt')

with open(file_path, 'r', encoding='utf-8') as file:
    document_text = file.read()

print(document_text)