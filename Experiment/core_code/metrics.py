from __future__ import annotations

from typing import Dict, List


def evaluate_predictions(rows: List[Dict[str, object]]) -> Dict[str, float]:
    total = len(rows)
    relevant = 0
    unsafe = 0
    irrelevant = 0
    accepted = 0
    dispatch_correct = 0
    anomaly_precision_hits = 0
    anomaly_precision_total = 0
    anomaly_recall_hits = 0
    anomaly_recall_total = 0

    for row in rows:
        prediction = row["prediction"]["action"]
        truth = row["ground_truth_action"]
        relevant_set = set(row["relevant_action_set"])
        unsafe_set = set(row["unsafe_action_set"])
        irrelevant_set = set(row["irrelevant_action_set"])
        if prediction in relevant_set:
            relevant += 1
        if prediction in unsafe_set:
            unsafe += 1
        if prediction in irrelevant_set:
            irrelevant += 1

        if row["clinician_review"] == "accept":
            accepted += 1
            if row["prediction"]["dispatch_target"] == row["expected_dispatch_target"]:
                dispatch_correct += 1

        predicted_anomalies = set(row["summary"]["dominant_anomalies"])
        truth_anomalies = set(row["expected_anomalies"])
        anomaly_precision_hits += len(predicted_anomalies & truth_anomalies)
        anomaly_precision_total += len(predicted_anomalies)
        anomaly_recall_hits += len(predicted_anomalies & truth_anomalies)
        anomaly_recall_total += len(truth_anomalies)

    return {
        "num_patient_weeks": total,
        "clinically_relevant_precision": round(relevant / total, 4) if total else 0.0,
        "unsafe_suggestion_rate": round(unsafe / total, 4) if total else 0.0,
        "irrelevant_suggestion_rate": round(irrelevant / total, 4) if total else 0.0,
        "clinician_acceptance_rate": round(accepted / total, 4) if total else 0.0,
        "dispatch_precision": round(dispatch_correct / accepted, 4) if accepted else 0.0,
        "anomaly_detection_precision": round(anomaly_precision_hits / anomaly_precision_total, 4)
        if anomaly_precision_total
        else 0.0,
        "anomaly_detection_recall": round(anomaly_recall_hits / anomaly_recall_total, 4)
        if anomaly_recall_total
        else 0.0,
    }
