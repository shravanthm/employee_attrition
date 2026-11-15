# Statistical Methodology — AttritionPulse AI

**Module:** Exploratory Data Analysis and Hypothesis Testing  
**Date:** 2026-11-15  

---

## 1. Statistical Philosophy & Research Rigor

AttritionPulse AI emphasizes statistically grounded risk detection rather than opaque heuristic scoring. All statistical analyses follow these core principles:
1. **Hypothesis Testing with Multiplicity Correction:** Whenever multiple factor comparisons are made, the Benjamini-Hochberg False Discovery Rate (FDR) adjustment is applied to prevent inflation of Type I errors ($\alpha = 0.05$).
2. **Dual Parametric & Non-Parametric Validation:** Both Student's t-test and the Mann-Whitney U test are reported alongside standardized Cohen's $d$ effect sizes.
3. **Interpretable Logit Modeling:** Multivariate logistic regression using statsmodels produces Odds Ratios with 95% Confidence Intervals.
4. **No Unsupported Causality:** Statistical correlations and hazard associations are explicitly documented as predictive indicators rather than direct causal drivers.

---

## 2. Factor Deterioration Index (FDI) Formulation

The Factor Deterioration Index measures the cumulative negative trajectory of an employee across primary psychological and organizational factors over rolling 3-month and 6-month horizons:

$$\text{FDI}_i = \frac{1}{K} \sum_{k=1}^K w_k \cdot \text{slope}_{k, 3m}$$

- Decreasing job satisfaction, work-life balance, and engagement contribute positively to FDI.
- Increasing overtime hours, stress levels, and absenteeism contribute positively to FDI.
- A positive and rising FDI indicates compounding distress and heightened probability of imminent departure.
