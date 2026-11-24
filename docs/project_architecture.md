# Project Architecture

```text
Resumes (PDF / DOCX / TXT) + Job Description + Skill Configuration
                         |
                         v
                Resume Text Parser
                         |
                         v
                Text Preprocessor
                         |
             +-----------+-----------+
             |                       |
             v                       v
       Skill Extractor         TF-IDF Vectorizer
             |                       |
             v                       v
       Required Skill %       Cosine Similarity %
             |                       |
             +-----------+-----------+
                         |
                         v
               Weighted Score Engine
                 60% skills / 40% text
                         |
                         v
                 Candidate Ranker
                         |
             +-----------+-----------+
             |                       |
             v                       v
        Streamlit UI            CSV / Excel
                         |
                         v
                 Human Review
```

## Data flow

1. The user supplies resume files, a job description, and a configurable skill dictionary.
2. The parser extracts text from each supported file type.
3. The preprocessor normalizes case, whitespace, and common noise.
4. A regex-based skill matcher detects required and preferred skills.
5. TF-IDF converts the job description and resume into weighted term vectors.
6. Cosine similarity measures textual overlap in vector space.
7. The scorer combines required-skill coverage (60%) and text similarity (40%).
8. The ranker sorts candidates and assigns review categories.
9. The CLI or Streamlit interface displays results and exports reports.

The system is a local educational simulation. It does not connect to an employer ATS.
