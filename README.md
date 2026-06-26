# 🎯 Career Coach AI

Career Coach AI is an intelligent career guidance application built using Python and Streamlit.

The application helps users explore different career paths, understand required skills, view learning roadmaps, discover projects, prepare for interviews, and learn about certifications, tools, job roles, and salary expectations.

---

## 🚀 Features

### 📚 Career Information
- Career Description
- Recommended For
- Skills Required
- Tools Used
- Learning Roadmap
- Project Ideas
- Interview Questions
- Certifications
- Job Roles
- Salary Insights

### 💼 Supported Careers

- Machine Learning Engineer
- Data Scientist
- Data Analyst
- AI Engineer
- Business Analyst
- Cloud Engineer
- Cybersecurity Analyst
- Graphic Designer
- Web Developer

---

## 🛠️ Tech Stack

- Python
- Streamlit
- JSON Knowledge Base

---

## 📂 Project Structure

```text
RAG-career-assistant/
│
├── data_json/
│   ├── ai_engineer.json
│   ├── business_analyst.json
│   ├── cloud_engineer.json
│   ├── cybersecurity.json
│   ├── data_analyst.json
│   ├── data_scientist.json
│   ├── graphic_designer.json
│   ├── ml_engineer.json
│   └── web_developer.json
│
├── rag/
│   ├── chunk_documents.py
│   ├── create_embeddings.py
│   ├── faiss_search.py
│   └── rag_chatbot.py
│
├── app.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd RAG-career-assistant
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Application

```bash
streamlit run app.py
```

---

## 💡 Example Questions

### Skills

```text
What skills are needed for a Data Scientist?
```

### Roadmap

```text
How do I become a Machine Learning Engineer?
```

### Projects

```text
Give projects for Data Analyst
```

### Interview Questions

```text
Give interview questions for AI Engineer
```

### Certifications

```text
What certifications should a Cybersecurity Analyst do?
```

### Salary

```text
What is the salary of a Cloud Engineer?
```

---

## 🔮 Future Improvements

- Career Recommendation Engine
- Career Comparison System
- Personalized Career Roadmaps
- Resume Guidance
- Mock Interview Simulator
- Learning Resource Recommendations
- Advanced NLP Search
- RAG-based Knowledge Retrieval

---

## 👨‍💻 Author

Nikhitha Bantu

BTech Student | AI & Machine Learning Enthusiast

---

## ⭐ Project Status

Currently under active development as part of an AI Career Guidance System.