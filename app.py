import streamlit as st
import json
from pathlib import Path

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="AI Career Coach",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 AI Career Coach")
st.write("Ask about skills, tools, projects, certifications, salaries, and more.")

# ==========================
# LOAD CAREER DATA
# ==========================

data_folder = Path("data_json")

careers = {}

for file in data_folder.glob("*.json"):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    careers[data["career"].lower()] = data

# ==========================
# SIDEBAR
# ==========================

st.sidebar.title("Available Careers")

for career in careers.values():
    st.sidebar.write("• " + career["career"])

# ==========================
# CHAT INPUT
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

            # ==========================
            # DESCRIPTION
            # ==========================
            if (
                "description" in q
                or "what does" in q
                or "about" in q
            ):

                st.subheader("Description")
                st.write(selected_career["description"])

            # ==========================
            # RECOMMENDED FOR
            # ==========================
            elif "recommended" in q:

                st.subheader("Recommended For")

                st.write("### Interests")
                for item in selected_career["recommended_for"]["interests"]:
                    st.write("•", item)

                st.write("### Strengths")
                for item in selected_career["recommended_for"]["strengths"]:
                    st.write("•", item)

            # ==========================
            # SKILLS
            # ==========================
            elif "skill" in q:

                st.subheader("Skills")

                skills = selected_career["skills"]

                if isinstance(skills, dict):

                    for category, items in skills.items():

                        st.write(f"### {category.replace('_', ' ').title()}")

                        for item in items:
                            st.write("•", item)

                else:

                    for item in skills:
                        st.write("•", item)

            # ==========================
            # TOOLS
            # ==========================
            elif "tool" in q:

                st.subheader("Tools")

                tools = selected_career["tools"]

                if isinstance(tools, dict):

                    for category, items in tools.items():

                        st.write(f"### {category.title()}")

                        for item in items:
                            st.write("•", item)

                else:

                    for item in tools:
                        st.write("•", item)

            # ==========================
            # PROJECTS
            # ==========================
            elif "project" in q:

                st.subheader("Projects")

                for item in selected_career["projects"]:
                    st.write("•", item)

            # ==========================
            # INTERVIEW QUESTIONS
            # ==========================
            elif (
                "interview" in q
                or "question" in q
            ):

                st.subheader("Interview Questions")

                for item in selected_career["interview_questions"]:
                    st.write("•", item)

            # ==========================
            # CERTIFICATIONS
            # ==========================
            elif (
                "certification" in q
                or "certificate" in q
                or "certifications" in q
            ):

                st.subheader("Certifications")

                for item in selected_career["certifications"]:
                    st.write("•", item)

            # ==========================
            # JOB ROLES
            # ==========================
            elif (
                "job role" in q
                or "jobs" in q
                or "career options" in q
                or "roles" in q
            ):

                st.subheader("Job Roles")

                for item in selected_career["job_roles"]:
                    st.write("•", item)

            # ==========================
            # SALARY
            # ==========================
            elif (
                "salary" in q
                or "package" in q
                or "pay" in q
            ):

                st.subheader("Salary")

                salary = selected_career["salary"]

                st.write("### Entry Level")
                st.write(salary["entry_level"])

                st.write("### Mid Level")
                st.write(salary["mid_level"])

                st.write("### Senior Level")
                st.write(salary["senior_level"])

            # ==========================
            # ROADMAP
            # ==========================
            elif (
                "roadmap" in q
                or "become" in q
                or "career path" in q
            ):

                st.subheader("Roadmap")

                for item in selected_career["roadmap"]:
                    st.write("•", item)

            # ==========================
            # DEFAULT RESPONSE
            # ==========================
            else:

                st.subheader(selected_career["career"])

                st.write("### Description")
                st.write(selected_career["description"])

                st.write("### Skills Categories")

                skills = selected_career["skills"]

                if isinstance(skills, dict):
                    for category in skills.keys():
                        st.write("•", category.replace("_", " ").title())

        else:

            st.warning(
                "Career not found.\n\n"
                "Try asking about one of the careers listed in the sidebar."
            )