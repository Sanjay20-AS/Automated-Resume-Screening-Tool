# Automated Resume Screening Tool

A student-built, Python-based ATS-style simulation that parses PDF, DOCX, and TXT resumes,
extracts configurable technical skills, compares resumes with a job description using TF-IDF
and cosine similarity, calculates explainable scores, ranks candidates, and exports CSV/Excel
reports. A Streamlit dashboard and command-line interface are included.

> **Educational project only:** This is not a real ATS and does not connect to company systems.
> Use synthetic or consented test data. Scores are decision-support signals only and must not
> be used as automated hiring or rejection decisions.

## Features

- Batch processing of PDF, DOCX, and TXT resumes
- Text cleaning and normalization
- Regex-based skill extraction with configurable aliases
- Required-skill coverage score
- TF-IDF + cosine similarity
- Weighted score: 60% skill coverage + 40% text similarity
- Candidate ranking and review categories
- Streamlit dashboard
- CLI execution
- CSV and formatted Excel exports
- Candidate score chart
- Synthetic sample resumes and job description
- Basic pytest suite

## Technology stack

Python, Pandas, NumPy, pdfplumber, python-docx, Regex, scikit-learn, TF-IDF,
cosine similarity, Streamlit, Matplotlib, openpyxl, pytest.

## Project structure

```text
Automated-Resume-Screening-Tool/
├── resumes/                 # 10 synthetic resumes: PDF, DOCX, TXT
├── data/                    # Job description and skill configuration
├── src/                     # Parsing, NLP, scoring, ranking, reporting modules
├── outputs/                 # Generated CSV and Excel reports
├── images/                  # Generated chart and dashboard preview
├── docs/                    # Architecture, methodology, interview prep
├── tests/                   # Pytest tests
├── app.py                   # Streamlit dashboard
├── main.py                  # CLI entry point
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup

Python 3.10 or newer is recommended.

### Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the command-line application

From the project root:

```bash
python main.py
```

Optional arguments:

```bash
python main.py --resumes resumes --job data/job_description.txt --skills data/required_skills.json --output outputs
```

The command prints the ranking and writes:
- `outputs/screening_results.csv`
- `outputs/screening_results.xlsx`
- `images/candidate_scores.png`

## Run the Streamlit dashboard

```bash
streamlit run app.py
```

Enable bundled synthetic resumes, optionally upload more files, edit the job description,
and select **Run screening**. Download CSV or Excel results from the page.

## Scoring

1. Required skill coverage = matched required skills / total required skills × 100.
2. Text similarity = TF-IDF cosine similarity × 100.
3. Final score = 0.60 × skill coverage + 0.40 × text similarity.

Default review bands:
- 75–100: Strong match – review
- 50–74.99: Moderate match – review
- Below 50: Low match – review

These are illustrative thresholds, not validated hiring criteria. Update the skill list in
`data/required_skills.json`. Scoring weights are passed to `calculate_resume_score()` in
`src/resume_scorer.py`.

## Run tests

```bash
pytest -q
```

## Sample output

A sample ranking and report files are included in `outputs/`. The results are generated from
the fictional resumes and fictional job description shipped with this project.

## Screenshots

See `images/` for the candidate score chart and dashboard preview.

## Limitations

- Scanned PDFs and image-only PDFs are not OCR processed.
- TF-IDF measures lexical overlap, not semantic fit.
- Regex matching depends on the skill dictionary and aliases.
- Parsing quality depends on resume layout and document structure.
- This project does not infer or score protected or sensitive characteristics.

## Responsible use

Do not use this project as the sole basis for employment decisions. Do not infer a person's
ability from missing extracted text. Review source documents, provide accessible alternatives,
validate the system for the intended role, assess disparate impact, and obtain appropriate
legal/privacy review before any real-world deployment.

## GitHub upload

1. Create a new public repository named `Automated-Resume-Screening-Tool`.
2. Extract this ZIP and open the project folder in VS Code.
3. Review `.gitignore` and ensure no private resumes or credentials are present.
4. Run the application and tests locally.
5. In the terminal:

```bash
git init
git add .
git commit -m "Build automated resume screening tool"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/Automated-Resume-Screening-Tool.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username.

## Suggested resume bullet

Built a Python-based resume screening simulation using pdfplumber, python-docx, Regex,
Scikit-learn TF-IDF, and cosine similarity; implemented explainable weighted scoring,
candidate ranking, a Streamlit dashboard, and CSV/Excel reporting.

## Future enhancements

OCR for scanned resumes, semantic embeddings, synonym expansion, database storage,
REST API, authentication, audit logging, and evaluation on a consented, representative dataset.
