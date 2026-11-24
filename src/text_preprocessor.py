"""Normalize resume text before matching."""
import re

def clean_text(text):
    text = str(text or "").replace("\x00", " ")
    text = text.lower()
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"[\r\t]+", " ", text)
    text = re.sub(r"[^a-z0-9+#.\s-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
