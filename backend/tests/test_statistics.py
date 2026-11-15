"""Tests for Phase 3 Statistical Analysis & Hypothesis Testing."""

import pytest
import numpy as np
import pandas as pd
from app.analytics.statistics import (
    calculate_descriptive_stats,
    run_hypothesis_tests,
    fit_interpretable_logistic_regression
)


def test_descriptive_statistics_calculation():
    df = pd.DataFrame({
        "job_satisfaction_score": [1.0, 2.0, 3.0, 4.0, 5.0],
        "overtime_hours": [0.0, 10.0, 20.0, 30.0, 40.0]
    })
    stats_df = calculate_descriptive_stats(df, ["job_satisfaction_score", "overtime_hours"])
    assert len(stats_df) == 2
    row_sat = stats_df[stats_df["factor"] == "job_satisfaction_score"].iloc[0]
    assert row_sat["mean"] == 3.0
    assert row_sat["median"] == 3.0
    assert row_sat["min"] == 1.0
    assert row_sat["max"] == 5.0


def test_hypothesis_testing_with_fdr():
    df_attrited = pd.DataFrame({
        "job_satisfaction_score": [1.0, 1.5, 2.0, 1.8, 2.2, 1.9],
        "overtime_hours": [35.0, 40.0, 42.0, 38.0, 45.0, 39.0]
    })
    df_retained = pd.DataFrame({
        "job_satisfaction_score": [4.0, 4.5, 4.2, 3.8, 4.9, 4.1],
        "overtime_hours": [5.0, 0.0, 8.0, 10.0, 2.0, 6.0]
    })
    results = run_hypothesis_tests(df_attrited, df_retained, ["job_satisfaction_score", "overtime_hours"])
    assert len(results) == 2
    assert (results["p_value_fdr_adjusted"] < 0.05).all()
    assert (results["significant_at_05"] == True).all()


def test_logistic_regression_odds_ratios():
    np.random.seed(42)
    n = 150
    sat = np.random.uniform(1.0, 5.0, n)
    wlb = np.random.uniform(1.0, 5.0, n)
    ot = np.random.exponential(12.0, n)
    mgr = np.random.uniform(1.5, 5.0, n)
    abs_rate = np.random.uniform(0.0, 20.0, n)
    stress = np.random.uniform(1.0, 5.0, n)
    
    # Linear predictor with noise to avoid perfect collinearity/separation
    z = -1.2 * sat - 0.8 * wlb + 0.05 * ot + 0.4 * stress + np.random.normal(0, 0.8, n)
    prob = 1 / (1 + np.exp(-z))
    attrition = (prob > 0.5).astype(int)

    df = pd.DataFrame({
        "job_satisfaction_score": sat,
        "work_life_balance_score": wlb,
        "overtime_hours": ot,
        "manager_support_score": mgr,
        "absence_rate": abs_rate,
        "stress_score": stress,
        "attrition_binary": attrition
    })

    logit_res = fit_interpretable_logistic_regression(df)
    assert "summary" in logit_res
    assert logit_res["pseudo_r2"] > 0
    assert len(logit_res["summary"]) >= 6
