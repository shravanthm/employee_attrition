# ML Methodology Documentation — AttritionPulse AI

**Module:** Machine Learning & Longitudinal Early-Warning Engine  
**Date:** 2026-11-15  

---

## 1. Problem Formulation

- **Prediction Objective:** Predict the probability that an active employee will voluntarily depart the organization within the next **90 days**.
- **Observation Unit:** An individual employee at monthly prediction cutoff $T$.
- **Temporal Integrity Rule:** Feature extraction uses historical observations $t \le T$ exclusively. No post-cutoff target leakage or future data contamination is permitted.

---

## 2. Feature Architecture

1. **Model A (Static Baseline):**
   - Demographics & Contractual: Job role, department, tenure, commute distance, months since last promotion.
2. **Model B (Temporal Model):**
   - Incorporates rolling metrics across the 12 behavioral factors:
     - 1-month rate of change ($\Delta_{1m}$)
     - 3-month and 6-month rolling averages
     - 3-month and 6-month Ordinary Least Squares trend slopes
     - Rolling volatility (standard deviation)
     - **Factor Deterioration Index (FDI)**
3. **Model C (Interaction Terms):**
   - Overtime $\times$ Work-life balance
   - Workload $\times$ Manager support
   - Stress $\times$ Recovery
4. **Model D (Full Production Ensemble):**
   - Calibrated combination of static, temporal, and interaction features.

---

## 3. Evaluation & Risk Scoring Framework

- **Performance Metrics:** ROC-AUC, PR-AUC, Precision, Recall, F1 Score, Brier Score.
- **Explainability:** SHAP (SHapley Additive exPlanations) TreeExplainer attribution scores for individual predictions.
- **Risk Tiers:**
  - **Low Risk:** $P \le 0.25$
  - **Moderate Risk:** $0.25 < P \le 0.50$
  - **High Risk:** $0.50 < P \le 0.75$
  - **Critical Risk:** $P > 0.75$
