"""Create a simple candidate score chart."""
from pathlib import Path
import matplotlib.pyplot as plt

def create_score_chart(rows, output_path):
    valid = [r for r in rows if r.get("status") == "Processed"]
    valid = sorted(valid, key=lambda r: r["final_score"], reverse=True)
    if not valid:
        return None
    names = [r["candidate_name"] for r in valid]
    scores = [r["final_score"] for r in valid]
    plt.figure(figsize=(10, 5))
    plt.barh(names[::-1], scores[::-1])
    plt.xlabel("Resume match score (0–100)")
    plt.title("Candidate Match Scores")
    plt.xlim(0, 100)
    plt.tight_layout()
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path, dpi=160)
    plt.close()
    return path
