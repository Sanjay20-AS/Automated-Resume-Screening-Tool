# Scoring Methodology

## 1. Required-skill coverage

`skill_match_pct = matched_required_skills / total_required_skills * 100`

The configured required skills are the denominator. If no required skills are configured,
the skill score is zero rather than dividing by zero.

## 2. TF-IDF and cosine similarity

The application vectorizes the job description and resume together using scikit-learn's
`TfidfVectorizer` with unigrams and bigrams. Cosine similarity is multiplied by 100 for
readability. This is lexical similarity, not a semantic understanding of experience.

## 3. Combined score

`final_score = 0.60 * skill_match_pct + 0.40 * similarity_pct`

The weights are configurable in `src/resume_scorer.py` when calling the scoring function.
They are demonstration choices, not statistically validated hiring weights.

## 4. Review categories

- 75–100: Strong match – review
- 50–74.99: Moderate match – review
- Below 50: Low match – review

These thresholds are configurable in `recommendation()`. They should be calibrated and
validated before any real-world use. No category automatically rejects a person.

## 5. Limitations and responsible use

- Keyword matching can miss synonyms, context, and skills expressed in unusual ways.
- PDF extraction can fail on scanned/image-only documents; OCR is not included.
- TF-IDF measures word overlap and does not understand meaning.
- Resume formatting and document quality can affect extraction.
- Candidate names and other personal details are not part of the score.
- Do not use this project as the sole basis for employment decisions. Human review,
  accessibility checks, bias assessment, validation, and legal review are necessary.
