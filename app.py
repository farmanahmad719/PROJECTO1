import streamlit as st
import matplotlib.pyplot as plt
from resume_parser import extract_text_from_pdf
from skills import job_skills

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="AI Smart Resume Analyzer",
    layout="wide"
)

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
.big-font {
    font-size:28px !important;
    font-weight:700;
}
.card {
    padding:20px;
    border-radius:15px;
    background-color:#f8f9fa;
    box-shadow:0px 4px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown("<div class='big-font'>🚀 AI Smart Resume Analyzer</div>", unsafe_allow_html=True)
st.caption("AI-powered resume evaluation & job role matching")

# ------------------ INPUT SECTION ------------------
col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])
with col2:
    job_role = st.selectbox("🎯 Select Job Role", list(job_skills.keys()))

# ------------------ PROCESS ------------------
if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)
    skills_required = job_skills[job_role]

    matched, missing = [], []
    for skill in skills_required:
        if skill in resume_text:
            matched.append(skill)
        else:
            missing.append(skill)

    match_percent = round(len(matched) / len(skills_required) * 100, 2)

    # ------------------ ATS SCORE (AI HEURISTIC) ------------------
    ats_score = min(95, match_percent + 10)

    # ------------------ DASHBOARD ------------------
    st.markdown("## 📊 Resume Analysis Dashboard")

    colA, colB, colC = st.columns(3)

    colA.metric("ATS Score", f"{ats_score}%")
    colB.metric("Skill Match", f"{match_percent}%")
    colC.metric("Missing Skills", len(missing))

    st.progress(match_percent / 100)

    # ------------------ CHART ------------------
    st.markdown("### 📈 Skill Distribution")
    fig, ax = plt.subplots()
    ax.bar(["Matched Skills", "Missing Skills"],
           [len(matched), len(missing)])
    st.pyplot(fig)

    # ------------------ RESULTS ------------------
    colX, colY = st.columns(2)

    with colX:
        st.markdown("### ✅ Matched Skills")
        st.success(", ".join(matched) if matched else "None")

    with colY:
        st.markdown("### ❌ Missing Skills")
        st.error(", ".join(missing) if missing else "None")

    # ------------------ AI FEEDBACK ------------------
    st.markdown("### 🧠 AI Feedback & Suggestions")

    suggestions = []

    if ats_score < 60:
        suggestions.append("Your resume lacks key skills. Add relevant projects.")
    if "project" not in resume_text:
        suggestions.append("Add a Projects section to strengthen your resume.")
    if "internship" not in resume_text:
        suggestions.append("Include internships or practical experience.")
    if len(resume_text.split()) < 300:
        suggestions.append("Resume content seems short. Add more details.")

    if suggestions:
        for s in suggestions:
            st.info("💡 " + s)
    else:
        st.success("Excellent resume! Minor improvements only.")

    st.markdown("---")
    st.caption("⚙ AI Analysis is based on NLP keyword matching & ATS heuristics.")
