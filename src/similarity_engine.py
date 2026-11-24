"""TF-IDF and cosine similarity between a resume and job description."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .text_preprocessor import clean_text

def calculate_similarity(resume_text, job_description):
    resume = clean_text(resume_text)
    job = clean_text(job_description)
    if not resume or not job:
        return 0.0
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
    matrix = vectorizer.fit_transform([job, resume])
    score = float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])
    return round(score * 100, 2)
