"""
Synthetic health data generator.
Produces a week of realistic health metrics for a single patient.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


def generate_weekly_data(
    seed: int = 42,
    patient_name: str = "Alex Johnson",
    start_date: datetime = None,
) -> pd.DataFrame:
    """Generate a synthetic week of health data."""
    rng = np.random.default_rng(seed)

    if start_date is None:
        # Default to the most recent Monday
        today = datetime.today()
        start_date = today - timedelta(days=today.weekday())

    dates = [start_date + timedelta(days=i) for i in range(7)]

    # Steps: target ~8,000/day with natural variance
    steps = rng.integers(4000, 14000, size=7).tolist()

    # Heart rate: resting BPM (60-90 normal range)
    heart_rate_avg = rng.integers(58, 95, size=7).tolist()
    heart_rate_max = [hr + rng.integers(20, 50) for hr in heart_rate_avg]

    # Sleep hours: 5.5 - 9.0 hrs
    sleep_hours = np.round(rng.uniform(5.5, 9.0, size=7), 1).tolist()

    # Sleep quality score: 1-10
    sleep_quality = rng.integers(4, 10, size=7).tolist()

    # Calories burned
    calories_burned = rng.integers(1600, 2800, size=7).tolist()

    # Calories consumed
    calories_consumed = rng.integers(1400, 3200, size=7).tolist()

    # Blood oxygen SpO2 (%): 94-100 normal
    spo2 = np.round(rng.uniform(94.0, 100.0, size=7), 1).tolist()

    # HRV (heart rate variability ms): higher = better recovery
    hrv = rng.integers(20, 80, size=7).tolist()

    # Stress level: 1-10
    stress = rng.integers(1, 10, size=7).tolist()

    # Water intake (liters)
    water_intake = np.round(rng.uniform(1.0, 3.5, size=7), 1).tolist()

    # Active minutes
    active_minutes = rng.integers(10, 90, size=7).tolist()

    df = pd.DataFrame(
        {
            "date": dates,
            "day": [d.strftime("%A") for d in dates],
            "steps": steps,
            "heart_rate_avg": heart_rate_avg,
            "heart_rate_max": heart_rate_max,
            "sleep_hours": sleep_hours,
            "sleep_quality": sleep_quality,
            "calories_burned": calories_burned,
            "calories_consumed": calories_consumed,
            "spo2": spo2,
            "hrv": hrv,
            "stress": stress,
            "water_intake": water_intake,
            "active_minutes": active_minutes,
        }
    )

    df["patient_name"] = patient_name
    return df


def compute_stats(df: pd.DataFrame) -> dict:
    """
    Compute deterministic summary statistics from the weekly data.
    The LLM never does math — we do it here.
    """
    calorie_balance = df["calories_burned"] - df["calories_consumed"]

    stats = {
        # Patient info
        "patient_name": df["patient_name"].iloc[0],
        "week_start": df["date"].iloc[0].strftime("%B %d"),
        "week_end": df["date"].iloc[-1].strftime("%B %d, %Y"),

        # Steps
        "avg_steps": int(df["steps"].mean()),
        "total_steps": int(df["steps"].sum()),
        "best_steps_day": df.loc[df["steps"].idxmax(), "day"],
        "best_steps_value": int(df["steps"].max()),
        "steps_goal_met_days": int((df["steps"] >= 10000).sum()),

        # Heart rate
        "avg_resting_hr": round(df["heart_rate_avg"].mean(), 1),
        "max_hr_recorded": int(df["heart_rate_max"].max()),
        "high_hr_days": int((df["heart_rate_avg"] > 85).sum()),

        # Sleep
        "avg_sleep": round(df["sleep_hours"].mean(), 1),
        "avg_sleep_quality": round(df["sleep_quality"].mean(), 1),
        "best_sleep_day": df.loc[df["sleep_hours"].idxmax(), "day"],
        "best_sleep_hours": df["sleep_hours"].max(),
        "poor_sleep_days": int((df["sleep_hours"] < 7).sum()),

        # Calories
        "avg_calories_burned": int(df["calories_burned"].mean()),
        "avg_calories_consumed": int(df["calories_consumed"].mean()),
        "avg_calorie_balance": int(calorie_balance.mean()),
        "total_calorie_balance": int(calorie_balance.sum()),

        # Blood oxygen
        "avg_spo2": round(df["spo2"].mean(), 1),
        "min_spo2": df["spo2"].min(),
        "low_spo2_days": int((df["spo2"] < 96).sum()),

        # HRV
        "avg_hrv": round(df["hrv"].mean(), 1),
        "best_hrv_day": df.loc[df["hrv"].idxmax(), "day"],
        "worst_hrv_day": df.loc[df["hrv"].idxmin(), "day"],

        # Stress
        "avg_stress": round(df["stress"].mean(), 1),
        "high_stress_days": int((df["stress"] >= 7).sum()),

        # Water
        "avg_water": round(df["water_intake"].mean(), 1),
        "hydration_goal_met": int((df["water_intake"] >= 2.5).sum()),

        # Activity
        "avg_active_minutes": int(df["active_minutes"].mean()),
        "total_active_minutes": int(df["active_minutes"].sum()),

        # Raw day-by-day for context
        "daily_summary": df[
            ["day", "steps", "sleep_hours", "heart_rate_avg", "stress", "hrv"]
        ].to_dict(orient="records"),
    }

    return stats
