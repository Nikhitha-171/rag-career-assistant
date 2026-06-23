import streamlit as st
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss

# ==========================
# Page Configuration
# ==========================
st.set_page_config(
    page_title="AI Career Assistant",
    page_icon="🎯",
    layout="wide"
)

# ==========================
# Header
# ==========================
st.title("🎯 AI Career Assistant")
st.write("Get career guidance, skills, roadmaps, and project ideas.")

# ==========================
# Sidebar
# ==========================
st.sidebar.title("Supported Careers")

st.sidebar.write("""
- Machine Learning Engineer
- Data Scientist
- Data Analyst
""")

# ==========================
# Load Documents
# ==========================
data_folder = Path("data")

all_text = ""

for file in data_folder.glob("*.txt"):
    with open(file, "r", encoding="utf-8") as f:
        all_text += f.read() + "\n"

# ==========================
# Chunk Documents
# ==========================
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = splitter.split_text(all_text)

# ==========================
# Create Embeddings
# ==========================
model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(chunks)

# ==========================
# Create FAISS Index
# ==========================
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

# ==========================
# Chat Input
# ==========================
question = st.chat_input("Ask a career question")

if question:

    with st.chat_message("user"):
        st.write(question)

    # Query Embedding
    query_embedding = model.encode([question])

    # Retrieve Top 2 Chunks
    distances, indices = index.search(query_embedding, 2)

    answer = ""

    for idx in indices[0]:
        answer += chunks[idx] + "\n\n"

    with st.chat_message("assistant"):
        st.write(answer)