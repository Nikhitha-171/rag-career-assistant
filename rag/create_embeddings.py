from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

# Read files
data_folder = Path("data")

all_text = ""

for file in data_folder.glob("*.txt"):
    with open(file, "r", encoding="utf-8") as f:
        all_text += f.read() + "\n"

# Chunking
splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)

chunks = splitter.split_text(all_text)

print(f"Total Chunks: {len(chunks)}")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create embeddings
embeddings = model.encode(chunks)

print("\nEmbedding Information:")

for i, embedding in enumerate(embeddings, start=1):
    print(f"Chunk {i} → Vector Length: {len(embedding)}")