# utils.py

import fitz  # PyMuPDF
import docx
import re
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return '\n'.join([para.text for para in doc.paragraphs])

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.lower().strip()

def calculate_similarity(resume_text, job_desc_text):
    tfidf = TfidfVectorizer(stop_words='english')
    vectors = tfidf.fit_transform([resume_text, job_desc_text])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])
    return round(similarity[0][0] * 100, 2)  # as percentage

def extract_keywords(text, top_n=20):
    cv = CountVectorizer(stop_words='english', max_features=1000)
    X = cv.fit_transform([text])
    keywords = cv.get_feature_names_out()
    freqs = X.toarray().flatten()
    
    keyword_freq = dict(zip(keywords, freqs))
    sorted_keywords = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)
    
    return [kw for kw, freq in sorted_keywords[:top_n]]

def find_missing_keywords(resume_keywords, jd_keywords):
    return list(set(jd_keywords) - set(resume_keywords))

