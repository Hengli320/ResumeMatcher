from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_matched_requirements(resume_keywords, job_requirements):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_keywords, job_requirements])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return job_requirements if similarity > 0.7 else None