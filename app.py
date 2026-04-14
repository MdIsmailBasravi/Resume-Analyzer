import streamlit as st
import PyPDF2
import re
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import cosine_similarity

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(page_title="AI ATS Resume Analyzer", layout="centered")

# ======================
# HEADER
# ======================
col1, col2 = st.columns([1, 8])

with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=55)

with col2:
    st.title("AI ATS Resume Analyzer")
    st.caption("AI-powered hiring intelligence system")

st.markdown("---")

# ======================
# CLEAN FUNCTION (SMART FILTER)
# ======================
def clean_text(text):
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    words = text.lower().split()

    noise_words = {
        "we","are","the","and","for","with","this","that","role",
        "should","have","looking","join","team","candidate",
        "including","will","job","work","experience","skills",
        "required","preferred","plus","ability","strong"
    }

    return {
        w for w in words
        if w not in ENGLISH_STOP_WORDS
        and w not in noise_words
        and len(w) > 2
    }

# ======================
# UPLOAD RESUME
# ======================
file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if file:

    reader = PyPDF2.PdfReader(file)
    resume_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            resume_text += text

    resume_text = resume_text.lower()
    st.success("Resume successfully processed")

    # ======================
    # JOB DESCRIPTION
    # ======================
    job_desc = st.text_area("Paste Job Description")

    if job_desc:

        job_desc = job_desc.lower()

        # ======================
        # NLP MATCH SCORE (CORE AI)
        # ======================
        vectorizer = TfidfVectorizer(stop_words="english")
        vectors = vectorizer.fit_transform([resume_text, job_desc])

        similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        match_score = round(similarity * 100, 2)

        # ======================
        # SKILL ENGINE
        # ======================
        skills = [
            "python","java","sql","machine learning",
            "flask","django","pandas","api","numpy"
        ]

        found_skills = [s for s in skills if s in resume_text]
        missing_skills = [s for s in skills if s not in resume_text]

        skill_score = round((len(found_skills) / len(skills)) * 100, 2)

        # ======================
        # EXPERIENCE ENGINE
        # ======================
        exp_keywords = ["project","built","developed","implemented","designed","deployed"]
        exp_score = sum(1 for w in exp_keywords if w in resume_text)
        exp_score = min(exp_score * 20, 100)

        # ======================
        # FINAL ATS SCORE (WEIGHTED MODEL)
        # ======================
        ats_score = round(
            (match_score * 0.5) +
            (skill_score * 0.3) +
            (exp_score * 0.2),
            2
        )

        # ======================
        # DECISION ENGINE
        # ======================
        if ats_score >= 75:
            decision = "✔ Strong Candidate — Highly Recommended"
        elif ats_score >= 50:
            decision = "⚠ Moderate Candidate — Needs Improvement"
        else:
            decision = "✖ Weak Candidate — Not Suitable"

        # ======================
        # DASHBOARD
        # ======================
        st.markdown("## 📊 ATS Evaluation Dashboard")

        col1, col2, col3 = st.columns(3)

        col1.metric("ATS Score", f"{ats_score}/100")
        col2.metric("Match Score", f"{match_score}/100")
        col3.metric("Skill Score", f"{skill_score}/100")

        st.progress(ats_score / 100)

        st.markdown("---")

        # ======================
        # DECISION
        # ======================
        st.markdown("### 🧠 Hiring Decision")
        st.info(decision)

        st.markdown("---")

        # ======================
        # SKILLS SECTION
        # ======================
        st.markdown("### 🛠 Skills Analysis")

        st.markdown("**✔ Found Skills**")
        if found_skills:
            for s in found_skills:
                st.write(f"- {s}")
        else:
            st.write("No major skills found")

        st.markdown("**✖ Missing Skills**")
        if missing_skills:
            for s in missing_skills:
                st.write(f"- {s}")

        st.markdown("---")

        # ======================
        # IMPROVEMENT PLAN
        # ======================
        st.markdown("### 📌 Improvement Plan")

        if missing_skills:
            for s in missing_skills:
                st.write(f"→ Improve: {s}")

        st.write("→ Add real-world deployed projects")
        st.write("→ Include measurable achievements")
        st.write("→ Optimize resume for ATS keywords")

        st.markdown("---")

        # ======================
        # SMART KEYWORDS
        # ======================
        st.markdown("### 🔍 Missing Keywords (Cleaned)")

        resume_words = clean_text(resume_text)
        job_words = clean_text(job_desc)

        missing_words = list(job_words - resume_words)

        if missing_words:
            for w in missing_words[:12]:
                st.write(f"- {w}")
        else:
            st.success("No important missing keywords detected")