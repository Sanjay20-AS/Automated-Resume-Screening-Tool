# Interview Preparation

## 1. What problem does the project solve?
It automates the first-pass organization of a batch of resumes by extracting text, identifying
configured skills, comparing text with a job description, ranking results, and exporting reports.

## 2. Why use pdfplumber?
It provides page-level text extraction from text-based PDFs and is straightforward to use.
It does not perform OCR on scanned image-only PDFs.

## 3. Why python-docx?
It reads paragraphs from DOCX documents through a simple Python API.

## 4. What is TF-IDF?
Term Frequency–Inverse Document Frequency weights terms by their frequency in a document
and how informative they are across the documents being compared.

## 5. What is cosine similarity?
It measures the cosine of the angle between two vectors. Here it provides a normalized
measure of lexical similarity between a job description and a resume.

## 6. Why combine skill matching and TF-IDF?
Skill matching provides explicit coverage of configured requirements, while TF-IDF captures
broader textual overlap. The combined score is more informative than either signal alone,
although it remains a simple heuristic.

## 7. What are the limitations?
Keyword matching misses context and synonyms; TF-IDF is not semantic; scanned PDFs need OCR;
and scores may reflect writing style or document quality. Human review is essential.

## 8. How would you improve it?
Add OCR, synonym/ontology support, validated semantic embeddings, configurable role templates,
robust entity extraction, audit logs, security controls, accessibility testing, and a formal
bias and validity assessment.

## 9. Why use modular Python files?
Separating parsing, preprocessing, skill extraction, similarity, scoring, ranking, and reporting
makes the project easier to test, maintain, and extend.

## 10. How do you test it?
Use pytest for supported file types, unsupported extensions, skill matching, score weighting,
empty inputs, and report generation.
