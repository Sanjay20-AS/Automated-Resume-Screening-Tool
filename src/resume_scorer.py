"""Combine skill match and text similarity into an explainable score."""
from .skill_extractor import calculate_skill_match

def calculate_resume_score(found_skills, required_skills, similarity_score,
                           skill_weight=0.60, similarity_weight=0.40):
    if not abs((skill_weight + similarity_weight) - 1.0) < 1e-9:
        raise ValueError("Weights must sum to 1.0")
    skill_score = calculate_skill_match(found_skills, required_skills)
    final_score = skill_score * skill_weight + similarity_score * similarity_weight
    return {
        "skill_match_pct": round(skill_score, 2),
        "similarity_pct": round(float(similarity_score), 2),
        "final_score": round(final_score, 2)
    }

def recommendation(score, strong_threshold=75, moderate_threshold=50):
    if score >= strong_threshold:
        return "Strong match – review"
    if score >= moderate_threshold:
        return "Moderate match – review"
    return "Low match – review"
