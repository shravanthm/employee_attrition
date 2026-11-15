"""Script to fit Kaplan-Meier curves and train Cox Proportional Hazards survival model."""

import os
import pandas as pd
from app.ml.survival import AttritionSurvivalEngine

def run_survival_pipeline():
    print("⏳ Running Phase 5 Survival Analysis Pipeline...")
    
    # Load synthetic data
    df_snaps = pd.read_csv("data/synthetic/monthly_snapshots.csv")
    df_events = pd.read_csv("data/synthetic/attrition_events.csv")
    df_emps = pd.read_csv("data/synthetic/employees.csv")
    
    # Calculate duration (days from hire date to event or observation end date)
    df_merged = df_emps.merge(df_events, left_on="id", right_on="employee_id")
    df_merged["hire_date"] = pd.to_datetime(df_merged["hire_date"])
    df_merged["event_date"] = pd.to_datetime(df_merged["event_date"])
    df_merged["duration_days"] = (df_merged["event_date"] - df_merged["hire_date"]).dt.days.clip(lower=1)
    df_merged["event_occurred"] = df_merged["censoring_status"]
    
    # Aggregate snapshot factors per employee
    agg_snaps = df_snaps.groupby("employee_id").agg({
        "job_satisfaction_score": "mean",
        "work_life_balance_score": "mean",
        "overtime_hours": "mean",
        "manager_support_score": "mean",
        "stress_score": "mean",
        "absence_rate": "mean"
    }).reset_index()
    
    survival_df = df_merged[["id", "duration_days", "event_occurred"]].merge(
        agg_snaps,
        left_on="id",
        right_on="employee_id"
    ).drop(columns=["id", "employee_id"])
    
    engine = AttritionSurvivalEngine(penalizer=0.1)
    
    # 1. Kaplan-Meier
    km_res = engine.fit_kaplan_meier(
        survival_df["duration_days"],
        survival_df["event_occurred"],
        label="Workforce Tenure Survival"
    )
    print(f"Kaplan-Meier Median Survival Days: {km_res['median_survival_time']}")
    
    # 2. Cox Proportional Hazards
    cox_res = engine.fit_cox_proportional_hazards(
        survival_df,
        duration_col="duration_days",
        event_col="event_occurred"
    )
    
    print(f"Cox PH Concordance Index: {cox_res['concordance_index']}")
    print("\n--- Cox Hazard Ratios ---")
    print(cox_res["summary"].to_string())
    
    # Save model and report
    os.makedirs("backend/app/ml/models", exist_ok=True)
    engine.save("backend/app/ml/models/cox_survival_model.pkl")
    cox_res["summary"].to_csv("reports/cox_hazard_ratios.csv", index=False)
    
    with open("docs/SURVIVAL_ANALYSIS.md", "w") as f:
        f.write("# Survival Analysis Report — AttritionPulse AI\n\n")
        f.write(f"**Concordance Index (C-Index):** {cox_res['concordance_index']}\n")
        f.write(f"**Partial AIC:** {cox_res['aic']}\n\n")
        f.write("## 1. Cox Proportional Hazards Regression Summary\n\n")
        f.write(cox_res["summary"].to_markdown(index=False))
        f.write("\n\n## 2. Multi-Horizon Forecast Horizon\n")
        f.write("Survival curves evaluate departure risk across 30, 60, 90, 180, and 365 calendar days.\n")
        
    print("✅ Phase 5 Survival Analysis complete. Written to docs/SURVIVAL_ANALYSIS.md")

if __name__ == "__main__":
    run_survival_pipeline()
