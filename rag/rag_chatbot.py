from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import faiss

# =========================
# Load Documents
# =========================
data_folder = Path("data")

all_text = ""

for file in data_folder.glob("*.txt"):
    with open(file, "r", encoding="utf-8") as f:
        all_text += f.read() + "\n"

# =========================
# Chunk Documents
# =========================
splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)

chunks = splitter.split_text(all_text)

print(f"Loaded {len(chunks)} chunks")

# =========================
# Create Embeddings
# =========================
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = embedding_model.encode(chunks)

# =========================
# Create FAISS Index
# =========================
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

print(f"FAISS Index Created with {index.ntotal} vectors")

# =========================
# Load LLM
# =========================
print("Loading LLM...")

generator = pipeline(
    "text-generation",
    model="google/flan-t5-base"
)

print("LLM Loaded Successfully!")

# =========================
# Ask Question
# =========================
query = input("\nAsk a career question: ")

# Convert query to embedding
query_embedding = embedding_model.encode([query])

# Search top 2 chunks
distances, indices = index.search(query_embedding, 2)

# Build context
context = ""

for idx in indices[0]:
    context += chunks[idx] + "\n"

print("\nRetrieved Context:")
print(context)

# =========================
# Generate Answer
# =========================
prompt = f"""
Based on the context below, answer the question.

Context:
{context}

Question:
{query}

Answer:
"""

response = generator(
    prompt,
    max_new_tokens=100,
    do_sample=False
)

print("\nAnswer:\n")

# Print full response for debugging
print(response)