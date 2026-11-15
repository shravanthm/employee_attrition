"""Tests for Phase 2 Longitudinal Data Engineering."""

import pytest
import pandas as pd
from datetime import date
from app.analytics.temporal import engineer_temporal_features, calculate_linear_slope
from scripts.generate_synthetic_data import generate_synthetic_data


def test_synthetic_data_generator():
    num_emps, num_snaps, num_events = generate_synthetic_data(num_employees=50, num_months=6, seed=123)
    assert num_emps == 50
    assert num_snaps >= 50
    assert num_events == 50

    df_snaps = pd.read_csv("data/synthetic/monthly_snapshots.csv")
    assert "job_satisfaction_score" in df_snaps.columns
    assert "overtime_hours" in df_snaps.columns
    assert "overtime_ratio" in df_snaps.columns
    assert "absence_rate" in df_snaps.columns
    assert (df_snaps["job_satisfaction_score"] >= 1.0).all()
    assert (df_snaps["job_satisfaction_score"] <= 5.0).all()


def test_linear_slope_calculation():
    rising = pd.Series([1.0, 2.0, 3.0, 4.0])
    assert calculate_linear_slope(rising) == pytest.approx(1.0, 0.01)

    falling = pd.Series([5.0, 4.0, 3.0, 2.0])
    assert calculate_linear_slope(falling) == pytest.approx(-1.0, 0.01)

    flat = pd.Series([3.0, 3.0, 3.0])
    assert calculate_linear_slope(flat) == pytest.approx(0.0, 0.01)


def test_temporal_feature_engineering_no_leakage():
    # Construct 4 monthly observations for 1 employee
    data = [
        {"employee_id": 1, "snapshot_month": "2026-01-01", "job_satisfaction_score": 4.0, "work_life_balance_score": 4.0, "overtime_hours": 10.0, "stress_score": 2.0, "engagement_score": 4.0, "manager_support_score": 4.0, "absence_rate": 0.0},
        {"employee_id": 1, "snapshot_month": "2026-02-01", "job_satisfaction_score": 3.5, "work_life_balance_score": 3.5, "overtime_hours": 20.0, "stress_score": 3.0, "engagement_score": 3.5, "manager_support_score": 3.8, "absence_rate": 5.0},
        {"employee_id": 1, "snapshot_month": "2026-03-01", "job_satisfaction_score": 2.5, "work_life_balance_score": 2.5, "overtime_hours": 35.0, "stress_score": 4.2, "engagement_score": 2.8, "manager_support_score": 3.0, "absence_rate": 10.0},
        {"employee_id": 1, "snapshot_month": "2026-04-01", "job_satisfaction_score": 1.5, "work_life_balance_score": 2.0, "overtime_hours": 45.0, "stress_score": 4.8, "engagement_score": 2.0, "manager_support_score": 2.5, "absence_rate": 15.0},
    ]
    df = pd.DataFrame(data)

    # Cutoff at March 1, 2026 — April must not be included
    features = engineer_temporal_features(df, cutoff_date="2026-03-01")
    assert len(features) == 1
    row = features.iloc[0]

    assert row["job_satisfaction_score"] == 2.5
    assert row["job_satisfaction_score_lag1"] == 3.5
    assert row["job_satisfaction_score_delta1m"] == pytest.approx(-1.0, 0.01)
    assert row["overtime_hours_delta1m"] == pytest.approx(15.0, 0.01)
    assert row["job_satisfaction_score_slope3m"] < 0  # deteriorating trend
    assert row["factor_deterioration_index"] > 0       # positive FDI signals rising deterioration
