# Phase 3 Report — Exploratory Data Analysis & Statistical Research

**Project:** AttritionPulse AI  
**Date:** 2026-11-15  
**Status:** Completed & Validated ✅  

---

## 1. Key Accomplishments

1. **Statistical Analysis Engine (`app.analytics.statistics`):**
   - Implemented `calculate_descriptive_stats` (Mean, Median, Std, Min, Max, Quantiles, Missing%).
   - Implemented `run_hypothesis_tests` utilizing dual Mann-Whitney U and Welch's t-test with **Benjamini-Hochberg False Discovery Rate (FDR)** multi-test correction.
   - Calculated standardized Cohen's $d$ effect sizes for all 12 factors.
   - Built interpretable multivariate logistic regression yielding Odds Ratios and 95% Confidence Intervals.

2. **Empirical Findings Summary:**
   - **Engagement & Satisfaction:** Statistically significant lower scores in attrited cohorts ($p < 10^{-6}$, Cohen's $d \approx -0.86$).
   - **Overtime & Stress:** Statistically significant elevations in departing employees ($p < 10^{-4}$, Cohen's $d \approx +0.60$).
   - **Factor Deterioration Index (FDI):** Statistically significant divergence between attrited ($\bar{x} = 0.123$) and retained ($\bar{x} = 0.008$) cohorts ($p = 1.37 \times 10^{-8}$, Cohen's $d = 1.071$).

3. **Generated Artifacts & Reports:**
   - [`reports/statistical_analysis_report.md`](file:///C:/Users/DELL/Projects/workforce-attrition-ai/reports/statistical_analysis_report.md)
   - `reports/descriptive_statistics.csv`
   - `reports/hypothesis_tests.csv`
   - `reports/logistic_regression_odds_ratios.csv`
   - [`docs/STATISTICAL_METHODOLOGY.md`](file:///C:/Users/DELL/Projects/workforce-attrition-ai/docs/STATISTICAL_METHODOLOGY.md)

4. **Testing:**
   - All 12 unit tests passing in pytest.
