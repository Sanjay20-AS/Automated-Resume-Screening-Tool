from pathlib import Path
import json
import pytest
from src.text_preprocessor import clean_text
from src.skill_extractor import extract_skills, calculate_skill_match
from src.resume_scorer import calculate_resume_score, recommendation
from src.resume_parser import extract_text

BASE = Path(__file__).resolve().parents[1]

def test_clean_text_normalizes_case_and_whitespace():
    assert clean_text(" Python   DEVELOPER ") == "python developer"

def test_skill_extraction_and_alias():
    config = json.loads((BASE / "data" / "required_skills.json").read_text())
    found = extract_skills("I use Python, SQL and sklearn.", config)
    assert "Python" in found
    assert "SQL" in found
    assert "Scikit-learn" in found

def test_skill_match_percentage():
    assert calculate_skill_match(["Python", "SQL"], ["Python", "SQL", "Git"]) == pytest.approx(66.67)

def test_empty_required_skills_returns_zero():
    assert calculate_skill_match(["Python"], []) == 0.0

def test_weighted_score():
    result = calculate_resume_score(["Python", "SQL"], ["Python", "SQL"], 50)
    assert result["skill_match_pct"] == 100
    assert result["final_score"] == 80

def test_weights_must_sum_to_one():
    with pytest.raises(ValueError):
        calculate_resume_score([], ["Python"], 50, 0.5, 0.4)

def test_recommendation_bands():
    assert recommendation(80).startswith("Strong")
    assert recommendation(60).startswith("Moderate")
    assert recommendation(30).startswith("Low")

def test_txt_parser():
    txt = BASE / "resumes" / "candidate_03_rohan_patel.txt"
    # Depending on extension cycling, candidate 3 is TXT.
    assert "Name:" in extract_text(txt)

def test_unsupported_file_extension(tmp_path):
    file = tmp_path / "resume.rtf"
    file.write_text("text")
    with pytest.raises(ValueError):
        extract_text(file)
