"""Configurable, boundary-aware skill extraction."""
import json
import re
from pathlib import Path
from .text_preprocessor import clean_text

def load_skill_config(config_path):
    return json.loads(Path(config_path).read_text(encoding="utf-8"))

def extract_skills(text, config):
    normalized = clean_text(text)
    aliases = {clean_text(k): v for k, v in config.get("aliases", {}).items()}
    found = set()
    all_skills = list(config.get("required", [])) + list(config.get("preferred", []))
    for skill in all_skills:
        key = clean_text(skill)
        pattern = r"(?<![a-z0-9])" + re.escape(key) + r"(?![a-z0-9])"
        if re.search(pattern, normalized):
            found.add(skill)
    for alias, canonical in aliases.items():
        pattern = r"(?<![a-z0-9])" + re.escape(alias) + r"(?![a-z0-9])"
        if re.search(pattern, normalized):
            found.add(canonical)
    return sorted(found, key=str.lower)

def calculate_skill_match(found_skills, required_skills):
    required = set(required_skills)
    if not required:
        return 0.0
    return round(100.0 * len(required.intersection(found_skills)) / len(required), 2)
