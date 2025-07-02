# app.py

import streamlit as st
from utils import (
    extract_text_from_pdf, extract_text_from_docx, clean_text,
    calculate_similarity, extract_keywords, find_missing_keywords
)

st.set_page_config(page_title="Resume Match Scorer", layout="centered")

st.title("📄 Resume Analyzer + Job Match Scorer")

# Upload Resume
resume_file = st.file_uploader("Upload your Resume (PDF or DOCX)", type=["pdf", "docx"])

# Paste or upload job description
job_description = st.text_area("Paste the Job Description here")

if st.button("Analyze Match"):
    if resume_file and job_description:
        # Extract resume text
        if resume_file.name.endswith('.pdf'):
            resume_text = extract_text_from_pdf(resume_file)
        else:
            resume_text = extract_text_from_docx(resume_file)

        # Clean text
        resume_clean = clean_text(resume_text)
        jd_clean = clean_text(job_description)

        # Similarity score
        score = calculate_similarity(resume_clean, jd_clean)
        st.success(f"✅ Match Score: {score} %")

        if score >= 70:
            st.info("Great! Your resume is a strong match.")
        elif score >= 40:
            st.warning("Moderate match. Consider tailoring your resume more.")
        else:
            st.error("Low match. Try adding more relevant skills/keywords.")

        # Keyword suggestion
        st.subheader("🔍 Suggested Keywords to Add")
        resume_keywords = extract_keywords(resume_clean, top_n=30)
        jd_keywords = extract_keywords(jd_clean, top_n=30)
        missing = find_missing_keywords(resume_keywords, jd_keywords)

        if missing:
            st.info("You may consider adding these keywords to better match the job:")
            st.write(", ".join(sorted(missing)))
        else:
            st.success("✅ Your resume already includes the key job description terms!")
    else:
        st.warning("Please upload a resume and paste a job description.")


