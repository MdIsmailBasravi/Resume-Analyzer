import streamlit as st
import PyPDF2

# ======================
# 🎨 PAGE CONFIG
# ======================
st.set_page_config(page_title="AI Career Gap Analyzer", page_icon="🤖", layout="centered")

st.title("🤖 AI Career Gap Analyzer")
st.caption("Analyze your resume, identify skill gaps, and match with job roles")

st.markdown("---")

# ======================
# 📄 FILE UPLOAD
# ======================
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

if uploaded_file is not None:

    # ======================
    # 📄 READ PDF
    # ======================
    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    text = text.lower()

    # ======================
    # 📄 VIEW TEXT
    # ======================
    with st.expander("📄 View Extracted Resume Text"):
        st.write(text)

    st.markdown("---")

    # ======================
    # 📊 SKILL ANALYSIS
    # ======================
    st.subheader("📊 Resume Analysis")

    skills = ["python", "java", "sql", "machine learning", "flask", "pandas"]

    found_skills = []
    missing_skills = []
    score = 0

    for skill in skills:
        if skill in text:
            found_skills.append(skill)
            score += 100 // len(skills)
        else:
            missing_skills.append(skill)

    # ======================
    # 📊 SCORE DISPLAY
    # ======================
    st.subheader("📊 Resume Score")
    st.progress(score / 100)
    st.write(f"### Score: {score}/100")

    if score >= 70:
        st.success("✅ Strong Resume")
    elif score >= 40:
        st.warning("⚠️ Average Resume")
    else:
        st.error("❌ Weak Resume")

    st.markdown("---")

    # ======================
    # ✅ SKILLS FOUND
    # ======================
    st.subheader("✅ Skills Found")

    if found_skills:
        st.write(", ".join(found_skills))
    else:
        st.write("No relevant skills found")

    # ======================
    # ❌ MISSING SKILLS
    # ======================
    st.subheader("❌ Missing Skills")

    if missing_skills:
        st.write(", ".join(missing_skills))
    else:
        st.success("No missing skills 🎉")

    st.markdown("---")

    # ======================
    # 💡 SUGGESTIONS
    # ======================
    st.subheader("💡 Improvement Suggestions")

    if missing_skills:
        st.warning("You should improve the following areas:")
        for skill in missing_skills:
            st.write(f"- Learn or add **{skill}**")
    else:
        st.success("🎉 Your resume covers all key skills!")

    st.info("Tip: Add real projects and deployment experience to stand out")

    st.markdown("---")

    # ======================
    # 🎯 JOB MATCHING
    # ======================
    st.subheader("🎯 Job Matching")

    job_desc = st.text_area("Paste Job Description here")

    if job_desc:
        job_desc = job_desc.lower()

        resume_words = set(text.split())
        job_words = set(job_desc.split())

        match = len(resume_words & job_words)
        total = len(job_words)

        match_percent = int((match / total) * 100) if total > 0 else 0

        st.subheader("📊 Job Match Score")
        st.progress(match_percent / 100)
        st.success(f"Match Score: {match_percent}%")

        missing_keywords = job_words - resume_words

        if missing_keywords:
            st.error("❌ Missing Keywords:")
            for word in list(missing_keywords)[:10]:
                st.write(f"- {word}")
        else:
            st.success("🎯 Excellent match with job description!")

    st.markdown("---")

    # ======================
    # 📌 FINAL FEEDBACK
    # ======================
    st.subheader("📌 Final Resume Feedback")

    if score >= 70:
        st.success("Your resume is strong but can still be improved for top companies.")
    elif score >= 40:
        st.warning("Your resume is average. Focus on adding key skills and projects.")
    else:
        st.error("Your resume needs major improvements to compete in the job market.")