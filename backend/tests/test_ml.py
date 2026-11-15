"""Tests for Phase 4 Machine Learning and SHAP Prediction Engine."""

import pytest
import pandas as pd
from app.ml.pipeline import AttritionPredictionEngine, classify_risk_tier


def test_risk_tier_classification():
    assert classify_risk_tier(0.15) == "Low"
    assert classify_risk_tier(0.35) == "Moderate"
    assert classify_risk_tier(0.65) == "High"
    assert classify_risk_tier(0.85) == "Critical"


def test_attrition_prediction_pipeline_and_shap():
    # Synthetic training batch
    data = []
    for i in range(120):
        sat = 1.0 + (i % 5)
        ot = (5 - sat) * 8
        attr = 1 if (sat <= 2 and ot >= 20) else 0
        data.append({
            "commute_minutes_one_way": 30.0,
            "months_since_promotion": 12,
            "job_satisfaction_score": sat,
            "work_life_balance_score": sat,
            "overtime_hours": ot,
            "department": "Sales" if i % 2 == 0 else "Research & Development",
            "job_role": "Sales Executive" if i % 2 == 0 else "Research Scientist",
            "attrition_binary": attr
        })
    df = pd.DataFrame(data)
    
    numeric_cols = ["commute_minutes_one_way", "months_since_promotion", "job_satisfaction_score", "work_life_balance_score", "overtime_hours"]
    categorical_cols = ["department", "job_role"]
    
    engine = AttritionPredictionEngine(model_type="xgboost")
    engine.train(df, df["attrition_binary"], numeric_cols, categorical_cols)
    
    # Test evaluation
    metrics = engine.evaluate(df, df["attrition_binary"])
    assert metrics["roc_auc"] >= 0.70
    assert "brier_score" in metrics
    
    # Test single prediction with SHAP
    test_sample = df.iloc[[0]].copy()
    pred_res = engine.predict_single_with_explanation(test_sample, top_k=3)
    
    assert "risk_probability" in pred_res
    assert "risk_category" in pred_res
    assert len(pred_res["top_explanations"]) > 0
    assert "shap_value" in pred_res["top_explanations"][0]
