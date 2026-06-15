import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

procedures = pd.read_csv(
    os.path.join(BASE_DIR, "procedures.csv"),
    skipinitialspace=True,
)
procedures.columns = [c.strip() for c in procedures.columns]
procedures["procedure-id"] = procedures["procedure-id"].str.strip()
procedures["title"] = procedures["title"].str.strip()
proc_lookup = dict(zip(procedures["procedure-id"], procedures["title"]))

COLORS = {
    "For": "#2ecc71",
    "Against": "#e74c3c",
    "Abstain": "#f39c12",
}

summary_rows = []

for folder in sorted(os.listdir(BASE_DIR)):
    folder_path = os.path.join(BASE_DIR, folder)
    csv_path = os.path.join(folder_path, "mistral-3.5.csv")
    if not os.path.isdir(folder_path) or not os.path.exists(csv_path):
        continue

    df = pd.read_csv(csv_path)
    counts = df["predicted_position"].value_counts()

    procedure_id = folder.strip()
    title = proc_lookup.get(procedure_id, "")

    n_for = int(counts.get("For", 0))
    n_against = int(counts.get("Against", 0))
    n_abstain = int(counts.get("Abstain", 0))
    total = n_for + n_against + n_abstain
    pct_for = round(n_for / total * 100, 1) if total else 0
    summary_rows.append({
        "procedure_id": procedure_id,
        "title": title,
        "for": n_for,
        "against": n_against,
        "abstain": n_abstain,
        "pct_for": pct_for,
    })
    chart_title = f"{procedure_id}\n{title}" if title else procedure_id

    labels = counts.index.tolist()
    sizes = counts.values.tolist()
    colors = [COLORS.get(lbl, "#95a5a6") for lbl in labels]

    fig, ax = plt.subplots(figsize=(7, 6))
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=None,
        colors=colors,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    )
    for at in autotexts:
        at.set_fontsize(11)
        at.set_fontweight("bold")

    legend_patches = [
        mpatches.Patch(color=COLORS.get(lbl, "#95a5a6"), label=f"{lbl} ({cnt})")
        for lbl, cnt in zip(labels, sizes)
    ]
    ax.legend(handles=legend_patches, loc="lower center", bbox_to_anchor=(0.5, -0.12),
              ncol=len(labels), fontsize=10)

    ax.set_title(chart_title, fontsize=11, fontweight="bold", pad=14, wrap=True)
    fig.tight_layout()

    out_path = os.path.join(folder_path, "piechart.png")
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out_path}")

summary_df = pd.DataFrame(summary_rows)
summary_path = os.path.join(BASE_DIR, "predicted_votes_summary.csv")
summary_df.to_csv(summary_path, index=False)
print(f"Saved summary: {summary_path}")
print("Done.")
