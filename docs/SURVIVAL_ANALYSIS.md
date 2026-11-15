# Survival Analysis Report — AttritionPulse AI

**Concordance Index (C-Index):** 0.6253
**Partial AIC:** 1245.56

## 1. Cox Proportional Hazards Regression Summary

| factor                  |   hazard_ratio |   hr_ci_lower_95 |   hr_ci_upper_95 |    p_value |   z_score |
|:------------------------|---------------:|-----------------:|-----------------:|-----------:|----------:|
| job_satisfaction_score  |       0.952182 |         0.736045 |         1.23179  | 0.709144   | -0.373006 |
| work_life_balance_score |       0.830768 |         0.665201 |         1.03754  | 0.102057   | -1.63496  |
| overtime_hours          |       1.0016   |         0.97527  |         1.02865  | 0.906098   |  0.117962 |
| manager_support_score   |       0.334999 |         0.160404 |         0.699633 | 0.00360705 | -2.91063  |
| stress_score            |       1.02292  |         0.685919 |         1.52551  | 0.911493   |  0.111156 |
| absence_rate            |       1.02778  |         0.962503 |         1.09749  | 0.413079   |  0.818487 |

## 2. Multi-Horizon Forecast Horizon
Survival curves evaluate departure risk across 30, 60, 90, 180, and 365 calendar days.
