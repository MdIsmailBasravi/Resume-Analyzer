import streamlit as st
import PyPDF2

# ======================
# PAGE SETUP
# ======================
st.set_page_config(page_title="Career Gap Analyzer")

st.title("Career Gap Analyzer")
st.write("Analyze your resume and identify improvement areas")

st.markdown("---")

# ======================
# FILE UPLOAD
# ======================
file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if file:

    reader = PyPDF2.PdfReader(file)
    text = ""

    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content

    text = text.lower()

    # ======================
    # SKILL ANALYSIS
    # ======================
    st.subheader("Analysis")

    skills = ["python", "java", "sql", "machine learning", "flask", "pandas"]

    found = []
    missing = []

    for skill in skills:
        if skill in text:
            found.append(skill)
        else:
            missing.append(skill)

    score = int((len(found) / len(skills)) * 100)

    # ======================
    # SCORE
    # ======================
    st.subheader("Score")
    st.write(f"{score} / 100")

    st.markdown("---")

    # ======================
    # DECISION
    # ======================
    st.subheader("Evaluation")

    if score >= 75:
        st.write("High chance of shortlisting")
    elif score >= 50:
        st.write("Moderate chance, improvement needed")
    else:
        st.write("Low chance, significant improvement required")

    st.markdown("---")

    # ======================
    # SKILLS FOUND
    # ======================
    st.subheader("Skills Identified")

    if found:
        for skill in found:
            st.write(f"- {skill}")
    else:
        st.write("No relevant skills identified")

    # ======================
    # MISSING SKILLS
    # ======================
    st.subheader("Skills to Improve")

    if missing:
        for skill in missing:
            st.write(f"- {skill}")
    else:
        st.write("All key skills covered")

    st.markdown("---")

    # ======================
    # ACTION PLAN
    # ======================
    st.subheader("Action Plan")

    if missing:
        for skill in missing:
            st.write(f"- Add or learn {skill}")
    else:
        st.write("Maintain current skill set and build projects")

    st.write("Focus on real-world projects and deployment experience")

    st.markdown("---")

    # ======================
    # JOB MATCHING
    # ======================
    st.subheader("Job Matching")

    job = st.text_area("Paste Job Description")

    if job:
        job = job.lower()

        resume_words = set(text.split())
        job_words = set(job.split())

        match = len(resume_words & job_words)
        total = len(job_words)

        percent = int((match / total) * 100) if total else 0

        st.write(f"Match Score: {percent} / 100")

        st.markdown("---")

        # ======================
        # INSIGHT
        # ======================
        st.subheader("Interpretation")

        if percent >= 70:
            st.write("Strong alignment with job requirements")
        elif percent >= 40:
            st.write("Partial alignment, improvement needed")
        else:
            st.write("Low alignment with this role")

        missing_words = job_words - resume_words

        if missing_words:
            st.subheader("Missing Keywords")
            for word in list(missing_words)[:10]:
                st.write(f"- {word}")