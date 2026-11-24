
from pathlib import Path
import tempfile
import json

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from src.candidate_ranker import screen_resumes
from src.report_generator import to_dataframe, export_reports

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

BASE = Path(__file__).resolve().parent

st.set_page_config(
    page_title="Automated Resume Screening Tool",
    page_icon="📄",
    layout="wide"
)

# --------------------------------------------------
# TOP HEADER
# --------------------------------------------------

st.title("📄 Automated Resume Screening Tool")

st.caption(
    "Educational ATS-style simulation • "
    "Explainable matching • Human review required"
)

st.markdown("---")

# --------------------------------------------------
# SIDEBAR - SCREENING INPUTS
# --------------------------------------------------

st.sidebar.header("Screening inputs")

default_job_description = """Python Developer – Entry-Level / Junior

We are seeking a Python Developer to build maintainable applications,
data-processing utilities, and automation workflows. The role involves
writing clean Python code, working with SQL databases, preparing and
analyzing data, and collaborating through Git.

Required skills: Python, SQL, Pandas, NumPy, Scikit-learn, Git.
Preferred skills: Regex, Flask, pytest, Matplotlib, REST API.

Responsibilities:
- Develop and maintain Python scripts and applications.
- Clean, transform, and analyze structured datasets.
- Work with SQL databases and APIs.
- Write tests and document code.
- Collaborate using Git and follow software engineering practices.

This job description is fictional and is intended for demonstrating
the screening workflow.
"""

job_file = BASE / "data" / "job_description.txt"

if job_file.exists():
    default_job_description = job_file.read_text(encoding="utf-8")

job_description = st.sidebar.text_area(
    "Job description",
    value=default_job_description,
    height=300
)

st.sidebar.markdown("---")

use_samples = st.sidebar.checkbox(
    "Include bundled synthetic sample resumes",
    value=True
)

uploads = st.sidebar.file_uploader(
    "Upload resumes (PDF, DOCX, TXT)",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

st.sidebar.caption(
    "200 MB per file • PDF, DOCX, TXT are supported"
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Scoring method: 60% required-skill coverage "
    "+ 40% TF-IDF similarity."
)

# --------------------------------------------------
# RUN SCREENING BUTTON
# --------------------------------------------------

run_screening = st.button(
    "🚀 Run Screening",
    type="primary",
    use_container_width=False
)

st.markdown(
    "Run screening to see candidate scores, skill coverage, "
    "ranking, and downloadable reports."
)

# --------------------------------------------------
# SCREENING EXECUTION
# --------------------------------------------------

if run_screening:

    resume_paths = []

    temp_dir = Path(
        tempfile.mkdtemp(prefix="resume_screen_")
    )

    if use_samples:
        sample_dir = BASE / "resumes"

        if sample_dir.exists():
            sample_resumes = sorted(
                p for p in sample_dir.iterdir()
                if p.is_file()
                and p.suffix.lower() in {".pdf", ".docx", ".txt"}
            )

            resume_paths.extend(sample_resumes)

    for uploaded_file in uploads or []:

        target_path = temp_dir / Path(uploaded_file.name).name

        target_path.write_bytes(
            uploaded_file.getbuffer()
        )

        resume_paths.append(target_path)

    if not job_description.strip():

        st.error("Please enter a job description.")

    elif not resume_paths:

        st.error(
            "Please upload at least one resume or "
            "enable bundled synthetic sample resumes."
        )

    else:

        try:
            with st.spinner(
                "Extracting resumes and calculating candidate scores..."
            ):

                results = screen_resumes(
                    resume_paths,
                    job_description,
                    BASE / "data" / "required_skills.json"
                )

                st.session_state["screening_rows"] = results
                st.session_state["screening_job"] = job_description

            st.success(
                f"Screening completed! "
                f"{len(results)} resumes analyzed."
            )

        except Exception as error:
            st.error(f"Screening failed: {error}")

# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

if "screening_rows" in st.session_state:

    rows = st.session_state["screening_rows"]

    df = to_dataframe(rows)

    valid_df = df[df["status"] == "Processed"].copy()

    st.markdown("---")

    st.header("📊 Screening Results")

    # --------------------------------------------------
    # OVERVIEW METRICS
    # --------------------------------------------------

    total_candidates = len(df)

    processed_candidates = len(valid_df)

    average_score = (
        valid_df["final_score"].mean()
        if processed_candidates else 0
    )

    strong_matches = (
        (valid_df["final_score"] >= 75).sum()
        if processed_candidates else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Resumes",
        total_candidates
    )

    c2.metric(
        "Successfully Processed",
        processed_candidates
    )

    c3.metric(
        "Average Match Score",
        f"{average_score:.2f}%"
    )

    c4.metric(
        "Strong Matches",
        int(strong_matches)
    )

    # --------------------------------------------------
    # CANDIDATE RANKING
    # --------------------------------------------------

    st.markdown("---")

    st.subheader("🏆 Candidate Ranking")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------
    # CANDIDATE SCORE CHART
    # --------------------------------------------------

    if not valid_df.empty:

        st.markdown("---")

        st.subheader("📈 Candidate-wise Skill Matching")

        skill_chart = valid_df.sort_values(
            "skill_match_pct",
            ascending=False
        ).set_index("candidate_name")[
            ["skill_match_pct"]
        ]

        st.bar_chart(skill_chart)

        st.subheader("📊 Overall Candidate Scores")

        score_chart = valid_df.sort_values(
            "final_score",
            ascending=False
        ).set_index("candidate_name")[
            ["final_score"]
        ]

        st.bar_chart(score_chart)

        # --------------------------------------------------
        # MATCHED AND MISSING SKILLS
        # --------------------------------------------------

        st.markdown("---")

        st.subheader("🔍 Candidate Skill Analysis")

        candidate_names = valid_df[
            "candidate_name"
        ].tolist()

        selected_candidate = st.selectbox(
            "Select a candidate",
            candidate_names
        )

        candidate = valid_df[
            valid_df["candidate_name"] == selected_candidate
        ].iloc[0]

        m1, m2, m3 = st.columns(3)

        m1.metric(
            "Final Score",
            f"{candidate['final_score']:.2f}%"
        )

        m2.metric(
            "Skill Match",
            f"{candidate['skill_match_pct']:.2f}%"
        )

        m3.metric(
            "Text Similarity",
            f"{candidate['similarity_pct']:.2f}%"
        )

        matched = [
            skill.strip()
            for skill in str(
                candidate["matched_required_skills"]
            ).split(",")
            if skill.strip()
        ]

        missing = [
            skill.strip()
            for skill in str(
                candidate["missing_required_skills"]
            ).split(",")
            if skill.strip()
        ]

        left, right = st.columns(2)

        with left:

            st.markdown("#### ✅ Matched Skills")

            if matched:
                for skill in matched:
                    st.success(skill)
            else:
                st.info("No required skills matched.")

        with right:

            st.markdown("#### ❌ Missing Skills")

            if missing:
                for skill in missing:
                    st.error(skill)
            else:
                st.success("All required skills matched!")

        # --------------------------------------------------
        # CANDIDATE COMPARISON
        # --------------------------------------------------

        st.markdown("---")

        st.subheader("⚖️ Compare Candidates")

        selected_candidates = st.multiselect(
            "Select candidates for comparison",
            candidate_names,
            default=candidate_names[:2]
        )

        if len(selected_candidates) >= 2:

            comparison = valid_df[
                valid_df["candidate_name"].isin(
                    selected_candidates
                )
            ]

            comparison = comparison.sort_values(
                "final_score",
                ascending=False
            )

            st.dataframe(
                comparison[
                    [
                        "candidate_name",
                        "final_score",
                        "skill_match_pct",
                        "similarity_pct",
                        "recommendation"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

        elif len(selected_candidates) == 1:

            st.info(
                "Select at least two candidates to compare."
            )

    # --------------------------------------------------
    # DOWNLOAD REPORTS
    # --------------------------------------------------

    st.markdown("---")

    st.subheader("📥 Download Screening Reports")

    col1, col2 = st.columns(2)

    csv_data = df.to_csv(
        index=False
    ).encode("utf-8")

    with col1:

        st.download_button(
            "⬇️ Download CSV Report",
            data=csv_data,
            file_name="screening_results.csv",
            mime="text/csv",
            use_container_width=True
        )

    with tempfile.TemporaryDirectory() as tmp:

        _, excel_path = export_reports(rows, tmp)

        with col2:

            st.download_button(
                "⬇️ Download Excel Report",
                data=Path(excel_path).read_bytes(),
                file_name="screening_results.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                ),
                use_container_width=True
            )

    # --------------------------------------------------
    # DISCLAIMER
    # --------------------------------------------------

    st.markdown("---")

    st.info(
        "⚠️ This is an educational ATS-style simulation. "
        "Scores are decision-support indicators, not hiring decisions. "
        "Human review is required."
    )

else:

    st.markdown("---")

    st.info(
        "👈 Configure your screening inputs in the sidebar "
        "and click **Run Screening** to see candidate scores, "
        "skill coverage, ranking, and downloadable reports."
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.caption(
    "Automated Resume Screening Tool | "
    "Python • NLP • TF-IDF • Cosine Similarity • Streamlit"
)
