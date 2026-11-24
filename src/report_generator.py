"""Export screening results to CSV and Excel."""
from pathlib import Path
import pandas as pd

def to_dataframe(rows):
    columns = ["rank", "candidate_name", "candidate_file", "final_score",
               "skill_match_pct", "similarity_pct", "recommendation",
               "matched_required_skills", "missing_required_skills",
               "extracted_skills", "status", "error"]
    return pd.DataFrame(rows, columns=columns)

def export_reports(rows, output_dir):
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    df = to_dataframe(rows)
    csv_path = output / "screening_results.csv"
    xlsx_path = output / "screening_results.xlsx"
    df.to_csv(csv_path, index=False)
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Candidate Ranking", index=False)
        for sheet in writer.sheets.values():
            sheet.freeze_panes = "A2"
            sheet.auto_filter.ref = sheet.dimensions
            for column_cells in sheet.columns:
                max_len = max(len(str(cell.value or "")) for cell in column_cells)
                sheet.column_dimensions[column_cells[0].column_letter].width = min(max_len + 2, 48)
    return csv_path, xlsx_path
