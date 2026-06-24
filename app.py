import streamlit as st
import json
from pathlib import Path

# ==========================
# Page Config
# ==========================
st.set_page_config(
    page_title="AI Career Assistant",
    page_icon="🎯"
)

st.title("🎯 AI Career Assistant")
st.write("Ask about skills, roadmaps, or projects for careers.")

# ==========================
# Load JSON Files
# ==========================
data_folder = Path("data_json")

careers = {}

for file in data_folder.glob("*.json"):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    careers[data["career"].lower()] = data

# ==========================
# Chat Input
# ==========================
question = st.chat_input("Ask a career question")

if question:

    with st.chat_message("user"):
        st.write(question)

    q = question.lower()

    selected_career = None

    for career_name in careers:
        if career_name in q:
            selected_career = careers[career_name]
            break

    with st.chat_message("assistant"):

        if selected_career:

            # Skills
            if "skill" in q:

                st.subheader("Skills")

                for skill in selected_career["skills"]:
                    st.write("•", skill)
            
            # Projects
            elif "project" in q:

                st.subheader("Projects")

                for project in selected_career["projects"]:
                    st.write("•", project)

            # Roadmap
            elif "roadmap" in q or "become" in q or "career path" in q:
                st.subheader("Roadmap")

                for step in selected_career["roadmap"]:
                    st.write("•", step)


            # Default
            else:

                st.subheader(selected_career["career"])

                st.write("### Skills")
                st.write(", ".join(selected_career["skills"]))

                st.write("### Roadmap")
                for step in selected_career["roadmap"]:
                    st.write("•", step)

                st.write("### Projects")
                for project in selected_career["projects"]:
                    st.write("•", project)

        else:

            st.warning(
                "Career not found.\n\n"
                "Try:\n"
                "- Machine Learning Engineer\n"
                "- Data Scientist\n"
                "- Data Analyst"
            )