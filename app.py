import streamlit as st
import json
import pandas as pd
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
# CAREER RECOMMENDATION ENGINE
# ==========================

st.sidebar.markdown("---")
st.sidebar.title("🎯 Find Your Career")

user_interests = st.sidebar.text_area(
    "Enter your interests and strengths",
    placeholder="Example: Coding, AI, Mathematics, Statistics"
)

if st.sidebar.button("Recommend Careers"):

    user_text = user_interests.lower()

    keyword_map = {
        "ai": "artificial intelligence",
        "coding": "programming",
        "math": "mathematics",
        "ml": "machine learning",
        "cyber security": "cybersecurity",
        "biz": "business"
    }

    for short, full in keyword_map.items():
        user_text = user_text.replace(short, full)

    user_keywords = [
        word.strip().lower()
        for word in user_text.split(",")
    ]

    scores = []

    for career in careers.values():

        score = 0

        recommendations = career.get("recommended_for", {})

        interests = recommendations.get("interests", [])
        strengths = recommendations.get("strengths", [])

        # Match interests
        for interest in interests:

            interest_lower = interest.lower()

            for keyword in user_keywords:

                if (
                    keyword in interest_lower
                    or interest_lower in keyword
                ):
                    score += 2
                    break

        # Match strengths
        for strength in strengths:

            strength_lower = strength.lower()

            for keyword in user_keywords:

                if (
                    keyword in strength_lower
                    or strength_lower in keyword
                ):
                    score += 1
                    break

        scores.append((career["career"], score))

    scores.sort(key=lambda x: x[1], reverse=True)

    st.sidebar.subheader("🏆 Top Career Matches")

    found_match = False

    for career_name, score in scores[:3]:

        if score > 0:
            found_match = True
            st.sidebar.success(
                f"{career_name} - Match Score: {score}"
            )

    if not found_match:
        st.sidebar.warning(
            "No matching careers found. Try entering more interests."
        )

# ==========================
# SKILL GAP ANALYZER
# ==========================

st.sidebar.markdown("---")
st.sidebar.title("📈 Skill Gap Analyzer")

target_career = st.sidebar.selectbox(
    "Target Career",
    [career["career"] for career in careers.values()]
)

user_skills = st.sidebar.text_area(
    "Your Current Skills",
    placeholder="Python, SQL, Pandas"
)

if st.sidebar.button("Analyze Skills"):

    selected = None

    for career in careers.values():

        if career["career"] == target_career:
            selected = career
            break

    required_skills = []

    for category in selected["skills"].values():
        required_skills.extend(category)

    user_skill_list = [
        skill.strip().lower()
        for skill in user_skills.split(",")
    ]

    have_skills = []
    missing_skills = []

    for skill in required_skills:

        if skill.lower() in user_skill_list:
            have_skills.append(skill)
        else:
            missing_skills.append(skill)

    score = int(
        (len(have_skills) / len(required_skills)) * 100
    )

    st.sidebar.success(
        f"Readiness Score: {score}%"
    )

    st.sidebar.write("### ✅ Skills You Have")

    for skill in have_skills:
        st.sidebar.write("•", skill)

    st.sidebar.write("### 🚀 Next Skills To Learn")

    for i, skill in enumerate(missing_skills, start=1):
        st.sidebar.write(f"{i}. {skill}")
    if score < 30:
       st.sidebar.warning(
        "Beginner Level - Focus on fundamentals."
       )

    elif score < 70:
       st.sidebar.info(
        "Intermediate Level - Build projects and strengthen skills."
       )

    else:
       st.sidebar.success(
        "Job Ready - Focus on internships and interview preparation."
       )
# ==========================
# CHAT INPUT
# ==========================

question = st.chat_input("Ask a career question")

if question:

    with st.chat_message("user"):
        st.write(question)

    q = question.lower()
    career_aliases = {
    "ml engineer": "machine learning engineer",
    "ai engineer": "artificial intelligence engineer",
    "data analyst": "data analyst",
    "data scientist": "data scientist",
    "web developer": "web developer",
    "cybersecurity": "cybersecurity analyst"
    }

    for alias, full_name in career_aliases.items():
        q = q.replace(alias, full_name)

    matched_careers = []

    for career_name, career_data in careers.items():

        if career_name in q:
             matched_careers.append(career_data)

    selected_career = matched_careers[0] if matched_careers else None

    with st.chat_message("assistant"):
       
       if (
        ("compare" in q or "vs" in q)
        and len(matched_careers) == 2
       ):
        
          career1 = matched_careers[0]
          career2 = matched_careers[1]

          comparison = {
            "Feature": [
              "Career",
              "Mid Salary",
              "Top Skills",
              "Tools",
              "Certifications",
              "Job Roles"
            ],

            career1["career"]: [
              career1["career"],
              career1["salary"]["mid_level"],

              ", ".join(
                list(career1["skills"].keys())[:3]
              ),

              ", ".join(
                career1["tools"][:5]
              ),

              ", ".join(
                career1["certifications"][:3]
              ),

              ", ".join(
                career1["job_roles"][:3]
              )
            ],

            career2["career"]: [
               career2["career"],
               career2["salary"]["mid_level"],

               ", ".join(
                 list(career2["skills"].keys())[:3]
               ),

               ", ".join(
                 career2["tools"][:5]
               ),

               ", ".join(
                 career2["certifications"][:3]
               ),

               ", ".join(
                 career2["job_roles"][:3]
               )
            ]
          }

          st.subheader("⚖️ Career Comparison")

          df = pd.DataFrame(comparison)

          st.table(df)


       elif selected_career:

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