from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

from baseline import (
    build_weekly_summary,
    dispatch_target_for_action,
    recommend_action,
    recommend_agentic,
    recommend_summary_only,
)
from metrics import evaluate_predictions
from simulator import generate_patient_weeks


def expected_dispatch_target(action: str) -> str:
    return dispatch_target_for_action(action)


def expected_anomalies_from_scenario(scenario: str) -> List[str]:
    mapping = {
        "stable_recovery": [],
        "spurious_single_day_outlier": [],
        "reduced_activity_with_sleep_disruption": ["activity_drop", "sleep_decline", "symptom_burden"],
        "rising_resting_hr_trend": ["rising_resting_hr"],
        "medication_nonadherence_pattern": ["nonadherence", "symptom_burden"],
        "possible_fluid_or_weight_related_decline": ["activity_drop", "symptom_burden"],
        "arrhythmia_like_pattern": ["rising_resting_hr", "symptom_burden"],
    }
    return mapping[scenario]


def clinician_review_label(prediction: str, row: Dict[str, object]) -> str:
    if prediction in set(row["unsafe_action_set"]):
        return "reject_as_unsafe"
    if prediction in set(row["irrelevant_action_set"]):
        return "reject_as_irrelevant"
    if prediction == row["ground_truth_action"]:
        return "accept"
    if prediction in set(row["relevant_action_set"]):
        return "revise_needed"
    return "reject_as_irrelevant"


def _evaluate_model(
    rows: List[Dict[str, object]],
    *,
    model_name: str,
    predictor,
    clinician_gate: bool = True,
) -> Dict[str, object]:
    evaluated_rows: List[Dict[str, object]] = []
    for row in rows:
        summary = build_weekly_summary(row)
        prediction = predictor(row, summary)
        expected_dispatch = expected_dispatch_target(row["ground_truth_action"])
        clinician_review = clinician_review_label(prediction["action"], row) if clinician_gate else "accept"
        evaluated_rows.append(
            {
                **row,
                "summary": summary,
                "prediction": prediction,
                "clinician_review": clinician_review,
                "expected_dispatch_target": expected_dispatch,
                "expected_anomalies": expected_anomalies_from_scenario(row["scenario"]),
            }
        )
    metrics = evaluate_predictions(evaluated_rows)
    return {
        "model_name": model_name,
        "metrics": metrics,
        "sample_cases": [
            {
                "patient_id": row["patient_id"],
                "week_index": row["week_index"],
                "scenario": row["scenario"],
                "ground_truth_action": row["ground_truth_action"],
                "predicted_action": row["prediction"]["action"],
                "clinician_review": row["clinician_review"],
                "dominant_anomalies": row["summary"]["dominant_anomalies"],
            }
            for row in evaluated_rows[:10]
        ],
    }


def run_all_models(num_patients: int, num_weeks: int, seed: int) -> Dict[str, object]:
    rows = generate_patient_weeks(num_patients=num_patients, num_weeks=num_weeks, seed=seed)
    models = {
        "threshold_template": lambda row, summary: recommend_action(row, summary),
        "summary_only_assistant": lambda row, summary: recommend_summary_only(row, summary),
        "agentic_rpm": lambda row, summary: recommend_agentic(row, summary, use_retrieval=True, use_history=True),
        "ablation_no_retrieval": lambda row, summary: recommend_agentic(
            row, summary, use_retrieval=False, use_history=True
        ),
        "ablation_no_patient_history": lambda row, summary: recommend_agentic(
            row, summary, use_retrieval=True, use_history=False
        ),
        "ablation_no_clinician_gate": lambda row, summary: recommend_agentic(
            row, summary, use_retrieval=True, use_history=True
        ),
    }
    outputs: Dict[str, object] = {
        "config": {"num_patients": num_patients, "num_weeks": num_weeks, "seed": seed},
        "models": {},
    }
    for name, predictor in models.items():
        outputs["models"][name] = _evaluate_model(
            rows,
            model_name=name,
            predictor=predictor,
            clinician_gate=(name != "ablation_no_clinician_gate"),
        )
    return outputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--num-patients", type=int, default=60)
    parser.add_argument("--num-weeks", type=int, default=8)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("Experiment/analysis/comparison_results.json"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = run_all_models(
        num_patients=args.num_patients,
        num_weeks=args.num_weeks,
        seed=args.seed,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2))
    printable = {name: block["metrics"] for name, block in results["models"].items()}
    print(json.dumps(printable, indent=2))
    print(f"Saved results to {args.output}")


if __name__ == "__main__":
    main()
