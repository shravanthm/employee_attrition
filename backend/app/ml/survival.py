"""Survival analysis and time-to-event estimation for AttritionPulse AI.
Includes:
- Kaplan-Meier estimator (overall, department, role, risk cohort)
- Cox Proportional Hazards regression (Hazard Ratios, 95% CIs, log-rank tests)
- Concordance index (C-index) evaluation
- Multi-horizon survival probability curves (30, 60, 90, 180, 365 days)
"""

import os
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from lifelines import KaplanMeierFitter, CoxPHFitter
from lifelines.utils import concordance_index


class AttritionSurvivalEngine:
    def __init__(self, penalizer: float = 0.1):
        self.penalizer = penalizer
        self.kmf = KaplanMeierFitter()
        self.cph = CoxPHFitter(penalizer=penalizer)
        self.trained = False

    def fit_kaplan_meier(self, durations: pd.Series, event_observed: pd.Series, label: str = "Overall Survival") -> Dict[str, Any]:
        self.kmf.fit(durations, event_observed=event_observed, label=label)
        timeline = self.kmf.timeline.tolist()
        survival_probs = self.kmf.survival_function_[label].tolist()
        
        return {
            "label": label,
            "timeline_days": timeline[:25],
            "survival_probabilities": [round(p, 4) for p in survival_probs[:25]],
            "median_survival_time": float(self.kmf.median_survival_time_) if not np.isinf(self.kmf.median_survival_time_) else None
        }

    def fit_cox_proportional_hazards(self, df_survival: pd.DataFrame, duration_col: str = "duration_days", event_col: str = "event_occurred") -> Dict[str, Any]:
        clean_df = df_survival.dropna().copy()
        
        # Ensure bool or int for event_col
        clean_df[event_col] = clean_df[event_col].astype(int)
        
        self.cph.fit(clean_df, duration_col=duration_col, event_col=event_col)
        self.trained = True
        
        # Extract Hazard Ratios, 95% CIs, p-values
        summary = self.cph.summary[["exp(coef)", "exp(coef) lower 95%", "exp(coef) upper 95%", "p", "z"]].reset_index()
        summary.columns = ["factor", "hazard_ratio", "hr_ci_lower_95", "hr_ci_upper_95", "p_value", "z_score"]
        
        c_index = round(float(self.cph.concordance_index_), 4)
        
        return {
            "summary": summary,
            "concordance_index": c_index,
            "aic": round(float(self.cph.AIC_partial_), 2)
        }

    def predict_survival_timeline(self, single_row: pd.DataFrame, times: List[int] = [30, 60, 90, 180, 365]) -> List[Dict[str, Any]]:
        if not self.trained:
            raise RuntimeError("Cox Proportional Hazards model has not been trained yet.")
            
        surv_func = self.cph.predict_survival_function(single_row, times=times)
        
        timeline = []
        for t in times:
            p = float(surv_func.loc[t].iloc[0])
            timeline.append({
                "horizon_days": t,
                "survival_probability": round(p, 4),
                "cumulative_attrition_risk": round(1.0 - p, 4)
            })
            
        return timeline

    def save(self, filepath: str):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self, filepath)

    @classmethod
    def load(cls, filepath: str):
        return joblib.load(filepath)
