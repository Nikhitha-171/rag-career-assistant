from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

data_folder = Path("data")

all_text = ""

for file in data_folder.glob("*.txt"):
    with open(file, "r", encoding="utf-8") as f:
        all_text += f.read() + "\n"

splitter = RecursiveCharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=20
)

chunks = splitter.split_text(all_text)

print(f"Total Chunks: {len(chunks)}\n")

for i, chunk in enumerate(chunks, start=1):
    print(f"Chunk {i}")
    print(chunk)
    print("-" * 50)