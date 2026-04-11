import streamlit as st
import PyPDF2

st.set_page_config(page_title="Resume Analyzer", page_icon="📄")

st.title("📄 Resume Analyzer")

uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    # Clean text
    text = text.lower()

    st.subheader("📄 Extracted Resume Text")
    st.write(text)

    # =========================
    # 📊 Resume Analysis
    # =========================
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

    # Progress bar
    st.progress(score / 100)

    # Score message
    if score >= 70:
        st.success(f"✅ Strong Resume! Score: {score}/100")
    elif score >= 40:
        st.warning(f"⚠️ Average Resume. Score: {score}/100")
    else:
        st.error(f"❌ Weak Resume. Score: {score}/100")

    # Skills display
    st.subheader("✅ Skills Found")
    st.write(", ".join(found_skills) if found_skills else "No skills found")

    st.subheader("❌ Missing Skills")
    st.write(", ".join(missing_skills) if missing_skills else "No missing skills")

    # =========================
    # 💡 Suggestions
    # =========================
    st.subheader("💡 Suggestions to Improve Resume")

    if missing_skills:
        st.write("You should consider adding these skills:")
        for skill in missing_skills:
            st.write(f"👉 Learn {skill}")
    else:
        st.success("🎉 Your resume covers all key skills!")

    # =========================
    # 🎯 Job Matching
    # =========================
    st.subheader("🎯 Job Matching")

    job_desc = st.text_area("Paste Job Description here")

    if job_desc:
        job_desc = job_desc.lower()

        resume_words = set(text.split())
        job_words = set(job_desc.split())

        match = len(resume_words & job_words)
        total = len(job_words)

        match_percent = int((match / total) * 100) if total > 0 else 0

        st.progress(match_percent / 100)
        st.write(f"### Match Score: {match_percent}%")

        missing_keywords = job_words - resume_words

        if missing_keywords:
            st.warning(
                "Missing Keywords: " + ", ".join(list(missing_keywords)[:10])
            )
        else:
            st.success("Great! Your resume matches the job very well 🎯")