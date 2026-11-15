# Model Evaluation Report — AttritionPulse AI

## 1. Algorithm & Feature Set Benchmark

| feature_set      | algorithm           |   roc_auc |   pr_auc |   precision |   recall |   f1_score |   brier_score |
|:-----------------|:--------------------|----------:|---------:|------------:|---------:|-----------:|--------------:|
| Model_A_Static   | logistic_regression |    0.5007 |   0.5059 |      0.451  |   0.697  |     0.5476 |        0.2683 |
| Model_A_Static   | random_forest       |    0.5548 |   0.5347 |      0.4681 |   0.6667 |     0.55   |        0.2545 |
| Model_A_Static   | xgboost             |    0.5267 |   0.4503 |      0.4615 |   0.5455 |     0.5    |        0.2965 |
| Model_B_Temporal | logistic_regression |    0.6198 |   0.659  |      0.4857 |   0.5152 |     0.5    |        0.249  |
| Model_B_Temporal | random_forest       |    0.6089 |   0.6708 |      0.5556 |   0.4545 |     0.5    |        0.2247 |
| Model_B_Temporal | xgboost             |    0.6154 |   0.68   |      0.5484 |   0.5152 |     0.5312 |        0.2695 |

**Selected Production Model:** LOGISTIC_REGRESSION with Temporal Feature Set (ROC-AUC: 0.6198)

## 2. Risk Categorization Thresholds
- **Low Risk:** Probability $\le 0.25$
- **Moderate Risk:** $0.25 <$ Probability $\le 0.50$
- **High Risk:** $0.50 <$ Probability $\le 0.75$
- **Critical Risk:** Probability $> 0.75$
