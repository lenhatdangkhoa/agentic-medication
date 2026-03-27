from __future__ import annotations

from typing import Dict, List


def dispatch_target_for_action(action: str) -> str:
    return {
        "monitor_only": "none",
        "repeat_measurement": "patient",
        "lab_order": "lab",
        "medication_review": "clinician",
        "follow_up_visit": "scheduling",
        "urgent_escalation": "clinician",
    }[action]


def build_weekly_summary(patient_week: Dict[str, object]) -> Dict[str, object]:
    profile = patient_week["profile"]
    summary_inputs = patient_week["weekly_summary_inputs"]
    anomalies: List[str] = []

    if summary_inputs["step_change_ratio"] < 0.7:
        anomalies.append("activity_drop")
    if summary_inputs["hr_change"] >= 8:
        anomalies.append("rising_resting_hr")
    if summary_inputs["sleep_change"] <= -0.8:
        anomalies.append("sleep_decline")
    if summary_inputs["avg_symptom_score"] >= 4.0:
        anomalies.append("symptom_burden")
    if summary_inputs["nonadherence_days"] >= 2:
        anomalies.append("nonadherence")

    return {
        "patient_id": patient_week["patient_id"],
        "week_index": patient_week["week_index"],
        "risk_tier": profile.risk_tier,
        "trend_summary": [
            f"Average steps: {summary_inputs['avg_steps']}",
            f"Average resting HR: {summary_inputs['avg_resting_hr']}",
            f"Average sleep duration: {summary_inputs['avg_sleep_duration']}",
            f"Average symptom score: {summary_inputs['avg_symptom_score']}",
        ],
        "dominant_anomalies": anomalies,
        "candidate_action_triggers": anomalies[:],
        "missing_data_note": "none",
    }


def recommend_action(patient_week: Dict[str, object], summary: Dict[str, object]) -> Dict[str, object]:
    profile = patient_week["profile"]
    anomalies = summary["dominant_anomalies"]
    history = patient_week["history"]

    action = "monitor_only"
    rationale = "No persistent concerning pattern was detected."

    if "rising_resting_hr" in anomalies and profile.risk_tier == "high":
        action = "urgent_escalation"
        rationale = "High-risk patient with sustained rise in resting heart rate."
    elif "nonadherence" in anomalies:
        action = "medication_review"
        rationale = "Multiple medication nonadherence days with symptom burden."
    elif "symptom_burden" in anomalies and "activity_drop" in anomalies:
        action = "follow_up_visit"
        rationale = "Declining activity plus symptoms indicates need for clinician follow-up."
    elif "sleep_decline" in anomalies and "activity_drop" in anomalies:
        action = "repeat_measurement"
        rationale = "Sleep and activity decline warrant repeat measurement before escalation."
    elif "rising_resting_hr" in anomalies:
        action = "lab_order"
        rationale = "Rising resting heart rate suggests lab follow-up."

    if "persistent_fatigue" in history["unresolved_issues"] and action == "monitor_only":
        action = "follow_up_visit"
        rationale = "Persistent unresolved fatigue justifies follow-up."

    dispatch_target = dispatch_target_for_action(action)

    safety_flags: List[str] = []
    if action == "medication_review" and "avoid_resting_hr_lowering_escalation" in profile.medication_constraints:
        safety_flags.append("medication_constraint_present")

    return {
        "action": action,
        "rationale": rationale,
        "supporting_evidence_items": anomalies,
        "safety_flags": safety_flags,
        "dispatch_target": dispatch_target,
    }


def recommend_summary_only(patient_week: Dict[str, object], summary: Dict[str, object]) -> Dict[str, object]:
    summary_inputs = patient_week["weekly_summary_inputs"]
    action = "monitor_only"
    rationale = "Weekly averages do not justify a stronger intervention."

    if summary_inputs["avg_symptom_score"] >= 5.2 and summary_inputs["hr_change"] >= 9:
        action = "urgent_escalation"
        rationale = "High symptom burden and elevated heart-rate trend indicate urgent review."
    elif summary_inputs["hr_change"] >= 6:
        action = "follow_up_visit"
        rationale = "Heart-rate trend warrants clinician follow-up."
    elif summary_inputs["nonadherence_days"] >= 2:
        action = "medication_review"
        rationale = "Repeated nonadherence suggests medication review."
    elif summary_inputs["step_change_ratio"] < 0.7 and summary_inputs["sleep_change"] <= -0.7:
        action = "repeat_measurement"
        rationale = "Activity and sleep decline justify repeat measurement."
    elif summary_inputs["avg_symptom_score"] >= 4.0:
        action = "lab_order"
        rationale = "Symptom burden suggests a lab workup."

    return {
        "action": action,
        "rationale": rationale,
        "supporting_evidence_items": summary["dominant_anomalies"],
        "safety_flags": [],
        "dispatch_target": dispatch_target_for_action(action),
    }


def _retrieval_context(patient_week: Dict[str, object], use_retrieval: bool, use_history: bool) -> Dict[str, object]:
    profile = patient_week["profile"]
    history = patient_week["history"]
    if not use_retrieval:
        return {
            "medication_constraints": [],
            "prior_abnormal_labs": [],
            "recent_clinician_actions": [],
            "unresolved_issues": [],
        }
    if not use_history:
        return {
            "medication_constraints": profile.medication_constraints,
            "prior_abnormal_labs": [],
            "recent_clinician_actions": [],
            "unresolved_issues": [],
        }
    return {
        "medication_constraints": profile.medication_constraints,
        "prior_abnormal_labs": history["prior_abnormal_labs"],
        "recent_clinician_actions": history["recent_clinician_actions"],
        "unresolved_issues": history["unresolved_issues"],
    }


def recommend_agentic(
    patient_week: Dict[str, object],
    summary: Dict[str, object],
    *,
    use_retrieval: bool = True,
    use_history: bool = True,
) -> Dict[str, object]:
    profile = patient_week["profile"]
    summary_inputs = patient_week["weekly_summary_inputs"]
    anomalies = set(summary["dominant_anomalies"])
    days = patient_week["daily_observations"]
    retrieved = _retrieval_context(patient_week, use_retrieval=use_retrieval, use_history=use_history)
    constraints = set(retrieved["medication_constraints"])
    prior_labs = set(retrieved["prior_abnormal_labs"])
    prior_actions = set(retrieved["recent_clinician_actions"])
    unresolved_issues = set(retrieved["unresolved_issues"])
    hr_spike_days = sum(1 for day in days if int(day["resting_hr"]) - int(summary_inputs["avg_resting_hr"]) >= 10)
    palpitations_days = sum(1 for day in days if "palpitations" in day["symptom_tags"])
    dizziness_days = sum(1 for day in days if "dizziness" in day["symptom_tags"])
    weight_gain_days = sum(1 for day in days if day["home_measurements"].get("weight_delta_kg", 0.0) >= 1.5)
    fatigue_days = sum(1 for day in days if "fatigue" in day["symptom_tags"])

    action = "monitor_only"
    rationale_parts: List[str] = []
    evidence: List[str] = list(summary["dominant_anomalies"])
    safety_flags: List[str] = []

    if (
        profile.risk_tier == "high"
        and ("rising_resting_hr" in anomalies or hr_spike_days >= 3)
        and (palpitations_days >= 2 or dizziness_days >= 1 or summary_inputs["avg_symptom_score"] >= 4.2)
    ):
        action = "urgent_escalation"
        rationale_parts.append("High-risk profile with repeated heart-rate instability and symptomatic burden.")
    elif weight_gain_days >= 2 and "activity_drop" in anomalies:
        action = "urgent_escalation" if profile.risk_tier == "high" else "lab_order"
        rationale_parts.append("Weight-related decline pattern suggests fluid or volume concern.")
    elif hr_spike_days == 1 and palpitations_days == 0 and summary_inputs["avg_symptom_score"] < 3.4:
        action = "repeat_measurement"
        rationale_parts.append("Single-day outlier without sustained symptoms suggests repeat measurement.")
    elif (
        summary_inputs["step_change_ratio"] >= 0.95
        and summary_inputs["avg_symptom_score"] <= 1.6
        and summary_inputs["sleep_change"] >= -0.2
    ):
        action = "monitor_only"
        rationale_parts.append("Stable recovery pattern supports monitoring only.")
    elif "rising_resting_hr" in anomalies and (
        palpitations_days >= 1 or summary_inputs["avg_symptom_score"] >= 4.2
    ):
        action = "follow_up_visit"
        rationale_parts.append("Heart-rate rise plus symptoms merits clinician follow-up.")
    elif "nonadherence" in anomalies:
        action = "medication_review"
        rationale_parts.append("Repeated nonadherence suggests medication review.")
        if fatigue_days >= 2:
            evidence.append("fatigue_after_nonadherence")
    elif {"activity_drop", "symptom_burden"} <= anomalies:
        action = "follow_up_visit"
        rationale_parts.append("Activity decline with symptom burden warrants follow-up.")
    elif {"activity_drop", "sleep_decline"} <= anomalies:
        action = "repeat_measurement"
        rationale_parts.append("Sleep and activity changes support repeat measurement.")
    elif "symptom_burden" in anomalies and (prior_labs or "monitor_renal_function" in constraints):
        action = "lab_order"
        rationale_parts.append("Symptoms plus prior lab risk support lab work.")
    elif "rising_resting_hr" in anomalies:
        action = "follow_up_visit" if profile.risk_tier != "low" else "lab_order"
        rationale_parts.append("Heart-rate trend justifies a non-urgent escalation.")

    if "persistent_fatigue" in unresolved_issues and action == "monitor_only":
        action = "follow_up_visit"
        rationale_parts.append("Unresolved fatigue remains open from prior weeks.")
    if "lab_order" in prior_actions and action == "lab_order":
        action = "follow_up_visit"
        rationale_parts.append("Recent lab order exists, so follow-up is preferred.")
    if "avoid_resting_hr_lowering_escalation" in constraints and action == "medication_review":
        action = "follow_up_visit"
        safety_flags.append("rerouted_due_to_medication_constraint")
        rationale_parts.append("Medication constraint prevents direct medication-review escalation.")
    if "monitor_renal_function" in constraints and action in {"follow_up_visit", "medication_review"}:
        evidence.append("renal_monitoring_constraint")
        if action == "follow_up_visit" and summary_inputs["avg_symptom_score"] >= 4.0:
            action = "lab_order"
            rationale_parts.append("Renal-monitoring constraint shifts follow-up toward lab evaluation.")
    if action == "monitor_only" and profile.risk_tier == "high" and summary_inputs["hr_change"] >= 5:
        action = "repeat_measurement"
        rationale_parts.append("High-risk profile with moderate heart-rate shift requires repeat measurement.")

    return {
        "action": action,
        "rationale": " ".join(rationale_parts) or "No high-priority intervention is warranted this week.",
        "supporting_evidence_items": sorted(set(evidence)),
        "safety_flags": safety_flags,
        "dispatch_target": dispatch_target_for_action(action),
    }
