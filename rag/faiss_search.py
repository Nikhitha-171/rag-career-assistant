from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss

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

# Embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(chunks)

# Create FAISS index
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

print("FAISS Index Created!")
print(f"Total vectors stored: {index.ntotal}")
# User query
query = "What skills are needed for ML Engineer?"

query_embedding = model.encode([query])

k = 4

distances, indices = index.search(query_embedding, k)

print("\nTop Matching Chunks:\n")

for idx in indices[0]:
    print(chunks[idx])
    print("-" * 50)