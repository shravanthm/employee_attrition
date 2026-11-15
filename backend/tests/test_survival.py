"""Tests for Phase 5 Survival Analysis and Hazard Estimation."""

import pytest
import pandas as pd
from app.ml.survival import AttritionSurvivalEngine


def test_survival_engine_km_and_cox():
    data = []
    for i in range(80):
        sat = 1.0 + (i % 5)
        ot = (5 - sat) * 5
        duration = 100 + (sat * 200) + (i * 10)
        event = 1 if (sat <= 2) else 0
        data.append({
            "duration_days": duration,
            "event_occurred": event,
            "job_satisfaction_score": sat,
            "work_life_balance_score": sat,
            "overtime_hours": ot,
            "manager_support_score": sat,
            "stress_score": 6 - sat,
            "absence_rate": (5 - sat) * 2
        })
    df = pd.DataFrame(data)
    
    engine = AttritionSurvivalEngine(penalizer=0.1)
    
    # 1. Kaplan-Meier
    km_res = engine.fit_kaplan_meier(df["duration_days"], df["event_occurred"])
    assert "timeline_days" in km_res
    assert len(km_res["survival_probabilities"]) > 0
    assert km_res["survival_probabilities"][0] >= 0.0
    
    # 2. Cox Proportional Hazards
    cox_res = engine.fit_cox_proportional_hazards(df)
    assert cox_res["concordance_index"] > 0.50
    assert "summary" in cox_res
    
    # 3. Survival Timeline Projection
    sample_row = df.iloc[[0]].drop(columns=["duration_days", "event_occurred"])
    timeline = engine.predict_survival_timeline(sample_row, times=[30, 90, 180])
    assert len(timeline) == 3
    assert timeline[0]["horizon_days"] == 30
    assert 0.0 <= timeline[0]["survival_probability"] <= 1.0
