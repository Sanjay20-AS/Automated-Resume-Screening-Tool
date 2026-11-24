"""Command-line entry point for the Automated Resume Screening Tool."""
import argparse
from pathlib import Path
from src.candidate_ranker import screen_resumes
from src.report_generator import export_reports, to_dataframe
from src.visualizer import create_score_chart

BASE = Path(__file__).resolve().parent

def run(resume_dir=None, job_path=None, config_path=None, output_dir=None):
    resume_dir = Path(resume_dir or BASE / "resumes")
    job_path = Path(job_path or BASE / "data" / "job_description.txt")
    config_path = Path(config_path or BASE / "data" / "required_skills.json")
    output_dir = Path(output_dir or BASE / "outputs")
    if not job_path.exists():
        raise FileNotFoundError(f"Job description not found: {job_path}")
    paths = sorted(p for p in resume_dir.iterdir()
                   if p.is_file() and p.suffix.lower() in {".pdf", ".docx", ".txt"})
    if not paths:
        raise ValueError(f"No supported resumes found in {resume_dir}")
    rows = screen_resumes(paths, job_path.read_text(encoding="utf-8"), config_path)
    csv_path, xlsx_path = export_reports(rows, output_dir)
    create_score_chart(rows, BASE / "images" / "candidate_scores.png")
    print(to_dataframe(rows)[["rank", "candidate_name", "final_score", "recommendation"]].to_string(index=False))
    print(f"\nCSV report: {csv_path}\nExcel report: {xlsx_path}")
    return rows

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Screen synthetic/sample resumes against a job description.")
    parser.add_argument("--resumes", default=str(BASE / "resumes"))
    parser.add_argument("--job", default=str(BASE / "data" / "job_description.txt"))
    parser.add_argument("--skills", default=str(BASE / "data" / "required_skills.json"))
    parser.add_argument("--output", default=str(BASE / "outputs"))
    args = parser.parse_args()
    run(args.resumes, args.job, args.skills, args.output)
