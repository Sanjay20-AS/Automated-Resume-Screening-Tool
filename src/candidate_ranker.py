"""Orchestrate parsing, matching, scoring, and ranking."""
from pathlib import Path
from .resume_parser import extract_text
from .skill_extractor import load_skill_config, extract_skills
from .similarity_engine import calculate_similarity
from .resume_scorer import calculate_resume_score, recommendation

def screen_resumes(resume_paths, job_description, config_path):
    config = load_skill_config(config_path)
    required = config.get("required", [])
    rows = []
    for path in resume_paths:
        path = Path(path)
        try:
            raw_text = extract_text(path)
            skills = extract_skills(raw_text, config)
            similarity = calculate_similarity(raw_text, job_description)
            scores = calculate_resume_score(skills, required, similarity)
            rows.append({
                "candidate_file": path.name,
                "candidate_name": _extract_name(raw_text, path.stem),
                "extracted_skills": ", ".join(skills),
                "matched_required_skills": ", ".join(sorted(set(skills) & set(required))),
                "missing_required_skills": ", ".join(sorted(set(required) - set(skills))),
                **scores,
                "recommendation": recommendation(scores["final_score"]),
                "status": "Processed",
                "error": ""
            })
        except Exception as exc:
            rows.append({
                "candidate_file": path.name, "candidate_name": path.stem,
                "extracted_skills": "", "matched_required_skills": "",
                "missing_required_skills": ", ".join(required),
                "skill_match_pct": 0.0, "similarity_pct": 0.0,
                "final_score": 0.0, "recommendation": "Manual review – processing error",
                "status": "Error", "error": str(exc)
            })
    rows.sort(key=lambda item: (item["status"] == "Processed", item["final_score"]), reverse=True)
    for rank, row in enumerate(rows, 1):
        row["rank"] = rank
    return rows

def _extract_name(text, fallback):
    for line in str(text).splitlines():
        if line.strip().lower().startswith("name:"):
            return line.split(":", 1)[1].strip() or fallback
    return fallback
