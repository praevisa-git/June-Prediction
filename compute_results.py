import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

EXCLUDE = {"2023-0226", "2026-0050"}

summary = pd.read_csv(os.path.join(BASE_DIR, "predicted_votes_summary.csv"))

result_rows = []

for _, row in summary.iterrows():
    procedure_id = str(row["procedure_id"]).strip()
    out = row.to_dict()

    if procedure_id in EXCLUDE:
        for col in ["actual_for", "actual_against", "actual_abstain",
                    "actual_category", "predicted_category", "category_match", "accuracy"]:
            out[col] = ""
        result_rows.append(out)
        continue

    votes_path = os.path.join(BASE_DIR, procedure_id, "member_votes.csv")
    pred_path = os.path.join(BASE_DIR, procedure_id, "mistral-3.5.csv")

    if not os.path.exists(votes_path):
        print(f"  No member_votes.csv for {procedure_id}, skipping accuracy")
        for col in ["actual_for", "actual_against", "actual_abstain",
                    "actual_category", "predicted_category", "category_match", "accuracy"]:
            out[col] = ""
        result_rows.append(out)
        continue

    actual = pd.read_csv(votes_path)
    actual_voted = actual[actual["position"] != "NONE"]

    actual_for = int((actual_voted["position"] == "FOR").sum())
    actual_against = int((actual_voted["position"] == "AGAINST").sum())
    actual_abstain = int((actual_voted["position"] == "ABSTAIN").sum())
    actual_category = "For" if actual_for > actual_against else "Against"

    n_for = row["for"] if pd.notna(row["for"]) and row["for"] != "" else 0
    n_against = row["against"] if pd.notna(row["against"]) and row["against"] != "" else 0
    predicted_category = "For" if int(n_for) > int(n_against) else "Against"
    category_match = predicted_category == actual_category

    # Per-MEP accuracy: join predicted with actual voted MEPs
    accuracy = ""
    if os.path.exists(pred_path):
        pred = pd.read_csv(pred_path)[["member_id", "predicted_position"]]
        merged = pred.merge(
            actual_voted[["mep_id", "position"]],
            left_on="member_id", right_on="mep_id",
            how="inner",
        )
        if len(merged) > 0:
            merged["correct"] = merged["predicted_position"].str.upper() == merged["position"]
            accuracy = round(merged["correct"].mean() * 100, 1)

    out["actual_for"] = actual_for
    out["actual_against"] = actual_against
    out["actual_abstain"] = actual_abstain
    out["actual_category"] = actual_category
    out["predicted_category"] = predicted_category
    out["category_match"] = category_match
    out["accuracy"] = accuracy
    result_rows.append(out)

result_cols = list(summary.columns) + [
    "actual_for", "actual_against", "actual_abstain",
    "actual_category", "predicted_category", "category_match", "accuracy",
]
result_df = pd.DataFrame(result_rows, columns=result_cols)
out_path = os.path.join(BASE_DIR, "result.csv")
result_df.to_csv(out_path, index=False)
print(f"Saved: {out_path}")
