"""Temporal feature engineering module for longitudinal employee snapshots.
Computes:
- previous month value
- 1-month change (delta)
- 3-month rolling average
- 6-month rolling average
- 3-month trend slope
- 6-month trend slope
- rolling volatility (std dev)
- Factor Deterioration Index (FDI)
"""

import numpy as np
import pandas as pd

FACTORS_TO_ENGINEER = [
    "job_satisfaction_score",
    "work_life_balance_score",
    "overtime_hours",
    "engagement_score",
    "manager_support_score",
    "absence_rate",
    "stress_score"
]


def calculate_linear_slope(series):
    """Calculates ordinary least squares linear slope over series."""
    valid = series.dropna()
    if len(valid) < 2:
        return 0.0
    x = np.arange(len(valid))
    y = valid.values
    slope, _ = np.polyfit(x, y, 1)
    return float(slope)


def engineer_temporal_features(df_snapshots: pd.DataFrame, cutoff_date: str = None) -> pd.DataFrame:
    """Takes monthly snapshots and computes temporal rolling metrics per employee up to cutoff_date.
    Ensures strict temporal separation (zero future data leakage).
    """
    df = df_snapshots.copy()
    df["snapshot_month"] = pd.to_datetime(df["snapshot_month"])
    
    if cutoff_date is not None:
        df = df[df["snapshot_month"] <= pd.to_datetime(cutoff_date)]
        
    df = df.sort_values(by=["employee_id", "snapshot_month"])
    
    engineered_rows = []
    
    for emp_id, group in df.groupby("employee_id"):
        group = group.sort_values(by="snapshot_month")
        
        # Last observed row for this employee at cutoff
        current_row = group.iloc[-1].to_dict()
        
        # For each factor, calculate rolling indicators
        for factor in FACTORS_TO_ENGINEER:
            if factor not in group.columns:
                continue
                
            vals = group[factor]
            
            # Current & Lag-1
            current_val = vals.iloc[-1]
            prev_val = vals.iloc[-2] if len(vals) >= 2 else current_val
            one_month_change = float(current_val - prev_val)
            
            # 3-month & 6-month rolling means
            roll_3m_mean = float(vals.tail(3).mean())
            roll_6m_mean = float(vals.tail(6).mean())
            
            # 3-month & 6-month slopes
            slope_3m = calculate_linear_slope(vals.tail(3))
            slope_6m = calculate_linear_slope(vals.tail(6))
            
            # Volatility
            volatility_3m = float(vals.tail(3).std(ddof=0)) if len(vals) >= 2 else 0.0
            
            current_row[f"{factor}_lag1"] = prev_val
            current_row[f"{factor}_delta1m"] = one_month_change
            current_row[f"{factor}_roll3m_mean"] = roll_3m_mean
            current_row[f"{factor}_roll6m_mean"] = roll_6m_mean
            current_row[f"{factor}_slope3m"] = slope_3m
            current_row[f"{factor}_slope6m"] = slope_6m
            current_row[f"{factor}_volatility3m"] = volatility_3m

        # Compute Factor Deterioration Index (FDI):
        # Deterioration increases when satisfaction/wlb/engagement drops, or overtime/stress/absenteeism increases
        fdi_components = []
        if "job_satisfaction_score_slope3m" in current_row:
            fdi_components.append(-current_row["job_satisfaction_score_slope3m"] * 1.5)
        if "work_life_balance_score_slope3m" in current_row:
            fdi_components.append(-current_row["work_life_balance_score_slope3m"] * 1.5)
        if "engagement_score_slope3m" in current_row:
            fdi_components.append(-current_row["engagement_score_slope3m"] * 1.2)
        if "overtime_hours_slope3m" in current_row:
            fdi_components.append(current_row["overtime_hours_slope3m"] * 0.1)
        if "stress_score_slope3m" in current_row:
            fdi_components.append(current_row["stress_score_slope3m"] * 1.0)
            
        fdi = float(np.mean(fdi_components)) if fdi_components else 0.0
        current_row["factor_deterioration_index"] = round(fdi, 4)
        
        engineered_rows.append(current_row)
        
    return pd.DataFrame(engineered_rows)
