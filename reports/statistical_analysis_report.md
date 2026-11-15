# Statistical Analysis & Research Report — AttritionPulse AI

**Sample Size:** 300 employee records
**Pseudo R-squared:** 0.1251

## 1. Descriptive Factor Summary

| factor                     |   mean |   median |    std |    min |    max |    q25 |    q75 |   missing_pct |
|:---------------------------|-------:|---------:|-------:|-------:|-------:|-------:|-------:|--------------:|
| job_satisfaction_score     |  3.083 |    3.23  |  0.967 |  1     |  5     |  2.488 |  3.762 |             0 |
| work_life_balance_score    |  3.109 |    3.245 |  1.009 |  1     |  4.94  |  2.558 |  3.772 |             0 |
| overtime_hours             | 14.141 |    9.95  | 13.712 |  0     | 61.5   |  3.575 | 20.775 |             0 |
| overtime_ratio             |  8.838 |    6.225 |  8.571 |  0     | 38.46  |  2.218 | 13.005 |             0 |
| engagement_score           |  3.367 |    3.455 |  0.869 |  1     |  5     |  2.848 |  4.053 |             0 |
| manager_support_score      |  3.578 |    3.58  |  0.314 |  2.72  |  4.43  |  3.35  |  3.782 |             0 |
| work_environment_score     |  3.902 |    3.89  |  0.523 |  3     |  4.8   |  3.45  |  4.353 |             0 |
| absence_rate               |  8.817 |   10     |  7.001 |  0     | 40     |  5     | 15     |             0 |
| stress_score               |  1.942 |    1.665 |  0.913 |  1     |  5     |  1.24  |  2.388 |             0 |
| wellbeing_score            |  2.956 |    3.08  |  0.953 |  1     |  4.7   |  2.428 |  3.59  |             0 |
| commute_minutes_one_way    | 37.75  |   30     | 18.38  | 15     | 90     | 30     | 45     |             0 |
| monthly_commute_hours      | 25.167 |   20     | 12.253 | 10     | 60     | 20     | 30     |             0 |
| factor_deterioration_index |  0.058 |    0.017 |  0.121 | -0.118 |  0.381 | -0.02  |  0.077 |             0 |

## 2. Hypothesis Testing (Attrited vs Retained Cohorts)

| factor                     |   attrited_mean |   retained_mean |   mann_whitney_u |   p_value_raw |   t_statistic |   cohens_d |   p_value_fdr_adjusted | significant_at_05   |
|:---------------------------|----------------:|----------------:|-----------------:|--------------:|--------------:|-----------:|-----------------------:|:--------------------|
| job_satisfaction_score     |           2.706 |           3.376 |           7135.5 |   1.30169e-07 |         -6.06 |     -0.736 |            3.38441e-07 | True                |
| work_life_balance_score    |           2.712 |           3.417 |           7124.5 |   1.19949e-07 |         -6.11 |     -0.743 |            3.38441e-07 | True                |
| overtime_hours             |          18.578 |          10.702 |          14370   |   9.46699e-06 |          4.95 |      0.598 |            1.39425e-05 | True                |
| overtime_ratio             |          11.61  |           6.689 |          14367   |   9.65253e-06 |          4.95 |      0.598 |            1.39425e-05 | True                |
| engagement_score           |           2.979 |           3.668 |           5982   |   8.69867e-12 |         -7.21 |     -0.861 |            1.13083e-10 | True                |
| manager_support_score      |           3.484 |           3.652 |           7669.5 |   5.06007e-06 |         -4.62 |     -0.556 |            1.09635e-05 | True                |
| work_environment_score     |           3.876 |           3.923 |          10522   |   0.462912    |         -0.77 |     -0.09  |            0.462912    | False               |
| absence_rate               |           9.771 |           8.077 |          12782.5 |   0.0181301   |          2.1  |      0.243 |            0.0235692   | True                |
| stress_score               |           2.238 |           1.713 |          14369.5 |   9.49437e-06 |          4.95 |      0.598 |            1.39425e-05 | True                |
| wellbeing_score            |           2.581 |           3.247 |           7115.5 |   1.12181e-07 |         -6.12 |     -0.744 |            3.38441e-07 | True                |
| commute_minutes_one_way    |          40.42  |          35.68  |          12637   |   0.0276409   |          2.21 |      0.26  |            0.0299443   | True                |
| monthly_commute_hours      |          26.947 |          23.787 |          12637   |   0.0276409   |          2.21 |      0.26  |            0.0299443   | True                |
| factor_deterioration_index |           0.123 |           0.008 |          15532.5 |   2.11973e-09 |          8.39 |      1.071 |            1.37782e-08 | True                |

## 3. Multivariate Logistic Regression (Odds Ratios)

| factor                  |   odds_ratio |   ci_lower_95 |   ci_upper_95 |   p_value |    std_err |
|:------------------------|-------------:|--------------:|--------------:|----------:|-----------:|
| Intercept               |    23.4661   |   3.20678e-18 |   1.71716e+20 | 0.886775  | 22.162     |
| job_satisfaction_score  |     0.631899 |   0.443933    |   0.899452    | 0.0108266 |  0.180134  |
| work_life_balance_score |     0.658674 |   0.473545    |   0.916179    | 0.0131404 |  0.168361  |
| overtime_hours          |     0.865759 |   0.0490593   |  15.2782      | 0.921597  |  1.46461   |
| manager_support_score   |     0.443598 |   0.173227    |   1.13596     | 0.0902172 |  0.479761  |
| absence_rate            |     1.00059  |   0.963466    |   1.03915     | 0.975531  |  0.0192909 |
| stress_score            |     8.91326  |   1.7041e-18  |   4.66206e+19 | 0.920761  | 21.9907    |

## 4. Key Empirical Insights
- **Factor Deterioration Index (FDI)** exhibits strong, statistically significant divergence between attrited and retained cohorts.
- Overtime hours and stress score correlate positively with higher odds of attrition.
- Job satisfaction and work-life balance scores exhibit Odds Ratios < 1.0 (protective retention factors).
- All reported p-values reflect Benjamini-Hochberg FDR adjustments.
