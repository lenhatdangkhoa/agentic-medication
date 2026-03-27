from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Dict, List


ACTIONS = [
    "monitor_only",
    "repeat_measurement",
    "lab_order",
    "medication_review",
    "follow_up_visit",
    "urgent_escalation",
]

SCENARIOS = [
    "stable_recovery",
    "spurious_single_day_outlier",
    "reduced_activity_with_sleep_disruption",
    "rising_resting_hr_trend",
    "medication_nonadherence_pattern",
    "possible_fluid_or_weight_related_decline",
    "arrhythmia_like_pattern",
]


@dataclass(frozen=True)
class PatientProfile:
    patient_id: str
    age_group: str
    sex: str
    condition_cluster: str
    risk_tier: str
    current_medications: List[str]
    medication_constraints: List[str]
    recent_lab_flags: List[str]
    baseline_activity_level: int
    baseline_resting_hr: int
    baseline_sleep_duration: float
    baseline_sleep_variability: float


def _choice(rng: random.Random, values: List[str]) -> str:
    return values[rng.randrange(len(values))]


def generate_patient_profiles(num_patients: int, seed: int) -> List[PatientProfile]:
    rng = random.Random(seed)
    profiles: List[PatientProfile] = []
    medication_pool = [
        "beta_blocker",
        "diuretic",
        "metformin",
        "ace_inhibitor",
        "statin",
        "none",
    ]
    lab_flags = ["elevated_a1c", "low_egfr", "high_ldl", "none"]
    condition_clusters = [
        "hypertension",
        "diabetes_risk",
        "heart_failure_risk",
        "arrhythmia_risk",
        "medication_adherence_risk",
    ]
    for index in range(num_patients):
        risk_tier = _choice(rng, ["low", "medium", "high"])
        med_count = 1 if risk_tier == "low" else rng.randint(1, 3)
        meds = rng.sample(medication_pool, med_count)
        constraints: List[str] = []
        if "beta_blocker" in meds:
            constraints.append("avoid_resting_hr_lowering_escalation")
        if "diuretic" in meds:
            constraints.append("monitor_fluid_and_electrolytes")
        if "ace_inhibitor" in meds:
            constraints.append("monitor_renal_function")
        profiles.append(
            PatientProfile(
                patient_id=f"patient_{index:04d}",
                age_group=_choice(rng, ["18_39", "40_59", "60_79", "80_plus"]),
                sex=_choice(rng, ["female", "male"]),
                condition_cluster=_choice(rng, condition_clusters),
                risk_tier=risk_tier,
                current_medications=meds,
                medication_constraints=constraints,
                recent_lab_flags=[flag for flag in rng.sample(lab_flags, 2) if flag != "none"],
                baseline_activity_level=rng.randint(4500, 11000),
                baseline_resting_hr=rng.randint(58, 88),
                baseline_sleep_duration=round(rng.uniform(6.2, 8.4), 1),
                baseline_sleep_variability=round(rng.uniform(0.4, 1.6), 2),
            )
        )
    return profiles


def _base_day(profile: PatientProfile, rng: random.Random) -> Dict[str, object]:
    return {
        "steps": max(500, int(rng.gauss(profile.baseline_activity_level, 900))),
        "resting_hr": max(45, int(rng.gauss(profile.baseline_resting_hr, 4))),
        "active_hr": max(70, int(rng.gauss(profile.baseline_resting_hr + 32, 8))),
        "sleep_start_time": round(rng.uniform(21.0, 25.0), 2),
        "sleep_duration_hours": round(max(3.5, rng.gauss(profile.baseline_sleep_duration, 0.8)), 2),
        "sleep_irregularity_score": round(max(0.0, rng.gauss(profile.baseline_sleep_variability, 0.3)), 2),
        "symptom_score": round(max(0.0, rng.gauss(1.5 if profile.risk_tier == "low" else 2.5, 1.0)), 2),
        "symptom_tags": [],
        "medication_adherence": 1,
        "home_measurements": {},
    }


def _apply_scenario(
    week_days: List[Dict[str, object]],
    scenario: str,
    profile: PatientProfile,
    rng: random.Random,
) -> None:
    if scenario == "stable_recovery":
        for day in week_days:
            day["steps"] = int(day["steps"] * 1.05)
            day["symptom_score"] = max(0.0, round(float(day["symptom_score"]) - 0.8, 2))
    elif scenario == "spurious_single_day_outlier":
        day = week_days[rng.randrange(len(week_days))]
        day["resting_hr"] = int(day["resting_hr"]) + 16
        day["symptom_tags"] = ["transient_outlier"]
    elif scenario == "reduced_activity_with_sleep_disruption":
        for day in week_days[2:]:
            day["steps"] = int(day["steps"] * 0.55)
            day["sleep_duration_hours"] = max(3.5, round(float(day["sleep_duration_hours"]) - 1.2, 2))
            day["sleep_irregularity_score"] = round(float(day["sleep_irregularity_score"]) + 1.0, 2)
            day["symptom_score"] = round(float(day["symptom_score"]) + 1.5, 2)
            day["symptom_tags"] = ["fatigue", "poor_sleep"]
    elif scenario == "rising_resting_hr_trend":
        for offset, day in enumerate(week_days):
            day["resting_hr"] = int(day["resting_hr"]) + (offset * 2)
            day["steps"] = int(day["steps"] * 0.85)
            if offset >= 3:
                day["symptom_score"] = round(float(day["symptom_score"]) + 1.2, 2)
                day["symptom_tags"] = ["palpitations"]
    elif scenario == "medication_nonadherence_pattern":
        for day in week_days[1:6]:
            if rng.random() < 0.6:
                day["medication_adherence"] = 0
                day["symptom_score"] = round(float(day["symptom_score"]) + 1.8, 2)
                day["symptom_tags"] = ["missed_meds", "symptom_rebound"]
    elif scenario == "possible_fluid_or_weight_related_decline":
        for day in week_days[3:]:
            day["steps"] = int(day["steps"] * 0.5)
            day["symptom_score"] = round(float(day["symptom_score"]) + 2.2, 2)
            day["symptom_tags"] = ["shortness_of_breath", "fatigue"]
            day["home_measurements"] = {"weight_delta_kg": round(rng.uniform(1.4, 3.2), 2)}
    elif scenario == "arrhythmia_like_pattern":
        for day in week_days:
            if rng.random() < 0.5:
                day["resting_hr"] = int(day["resting_hr"]) + rng.randint(15, 28)
                day["active_hr"] = int(day["active_hr"]) + rng.randint(10, 20)
                day["symptom_score"] = round(float(day["symptom_score"]) + 1.7, 2)
                day["symptom_tags"] = ["palpitations", "dizziness"]
    else:
        raise ValueError(f"Unknown scenario: {scenario}")


def _history_for_week(profile: PatientProfile, week_index: int, rng: random.Random) -> Dict[str, object]:
    prior_actions = []
    if week_index > 0 and rng.random() < 0.35:
        prior_actions.append(_choice(rng, ["lab_order", "follow_up_visit", "medication_review"]))
    return {
        "prior_weeks": min(week_index, 4),
        "recent_clinician_actions": prior_actions,
        "prior_clinician_rejections": [] if rng.random() < 0.8 else ["lab_order"],
        "prior_abnormal_labs": profile.recent_lab_flags,
        "unresolved_issues": [] if rng.random() < 0.7 else ["persistent_fatigue"],
    }


def _ground_truth(profile: PatientProfile, scenario: str) -> Dict[str, object]:
    if scenario == "stable_recovery":
        primary_action = "monitor_only"
        relevant = {"monitor_only"}
        unsafe = {"urgent_escalation"}
    elif scenario == "spurious_single_day_outlier":
        primary_action = "repeat_measurement"
        relevant = {"repeat_measurement", "monitor_only"}
        unsafe = {"urgent_escalation"}
    elif scenario == "reduced_activity_with_sleep_disruption":
        primary_action = "follow_up_visit"
        relevant = {"follow_up_visit", "repeat_measurement"}
        unsafe = set()
    elif scenario == "rising_resting_hr_trend":
        primary_action = "follow_up_visit" if profile.risk_tier != "high" else "urgent_escalation"
        relevant = {"follow_up_visit", primary_action, "lab_order"}
        unsafe = set()
    elif scenario == "medication_nonadherence_pattern":
        primary_action = "medication_review"
        relevant = {"medication_review", "follow_up_visit", "repeat_measurement"}
        unsafe = set()
    elif scenario == "possible_fluid_or_weight_related_decline":
        primary_action = "urgent_escalation" if profile.risk_tier == "high" else "lab_order"
        relevant = {"urgent_escalation", "lab_order", "follow_up_visit"}
        unsafe = {"monitor_only"}
    elif scenario == "arrhythmia_like_pattern":
        primary_action = "urgent_escalation"
        relevant = {"urgent_escalation", "follow_up_visit"}
        unsafe = {"monitor_only"}
    else:
        raise ValueError(f"Unknown scenario: {scenario}")

    if "avoid_resting_hr_lowering_escalation" in profile.medication_constraints and scenario in {
        "stable_recovery",
        "spurious_single_day_outlier",
    }:
        unsafe.add("medication_review")
    if "monitor_renal_function" in profile.medication_constraints:
        relevant.add("lab_order")

    irrelevant = set(ACTIONS) - relevant - unsafe
    return {
        "ground_truth_action": primary_action,
        "relevant_action_set": sorted(relevant),
        "unsafe_action_set": sorted(unsafe),
        "irrelevant_action_set": sorted(irrelevant),
    }


def _summary_from_week(profile: PatientProfile, week_days: List[Dict[str, object]], scenario: str) -> Dict[str, object]:
    steps = [int(day["steps"]) for day in week_days]
    resting_hr = [int(day["resting_hr"]) for day in week_days]
    sleep_duration = [float(day["sleep_duration_hours"]) for day in week_days]
    symptoms = [float(day["symptom_score"]) for day in week_days]
    adherence = [int(day["medication_adherence"]) for day in week_days]
    return {
        "avg_steps": round(sum(steps) / len(steps), 1),
        "avg_resting_hr": round(sum(resting_hr) / len(resting_hr), 1),
        "avg_sleep_duration": round(sum(sleep_duration) / len(sleep_duration), 2),
        "avg_symptom_score": round(sum(symptoms) / len(symptoms), 2),
        "nonadherence_days": adherence.count(0),
        "risk_tier": profile.risk_tier,
        "scenario_hint": scenario,
        "step_change_ratio": round((sum(steps) / len(steps)) / profile.baseline_activity_level, 2),
        "hr_change": round((sum(resting_hr) / len(resting_hr)) - profile.baseline_resting_hr, 1),
        "sleep_change": round((sum(sleep_duration) / len(sleep_duration)) - profile.baseline_sleep_duration, 2),
    }


def generate_patient_weeks(num_patients: int, num_weeks: int, seed: int) -> List[Dict[str, object]]:
    rng = random.Random(seed)
    profiles = generate_patient_profiles(num_patients=num_patients, seed=seed)
    rows: List[Dict[str, object]] = []
    for profile in profiles:
        for week_index in range(num_weeks):
            scenario = _choice(rng, SCENARIOS)
            week_days = [_base_day(profile, rng) for _ in range(7)]
            _apply_scenario(week_days, scenario=scenario, profile=profile, rng=rng)
            ground_truth = _ground_truth(profile, scenario)
            rows.append(
                {
                    "patient_id": profile.patient_id,
                    "week_index": week_index,
                    "profile": profile,
                    "history": _history_for_week(profile, week_index, rng),
                    "scenario": scenario,
                    "daily_observations": week_days,
                    "weekly_summary_inputs": _summary_from_week(profile, week_days, scenario),
                    **ground_truth,
                }
            )
    return rows
