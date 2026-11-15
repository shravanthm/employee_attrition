"""ML Pipeline, Preprocessor, Trainer, and Evaluator for AttritionPulse AI.
Supports:
- Model A: Static baseline
- Model B: Temporal model (changes, rolling averages, slopes, volatility)
- Model C: Interaction model
- Model D: Full model
- Algorithms: Logistic Regression, Random Forest, XGBoost
- Evaluation: ROC-AUC, PR-AUC, Precision, Recall, F1, Brier Score
- SHAP TreeExplainer & LinearExplainer integration
- Configurable risk thresholds: Low (<=0.25), Moderate (0.25-0.50), High (0.50-0.75), Critical (>0.75)
"""

import os
from typing import Any

import joblib
import numpy as np
import pandas as pd
import shap
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBClassifier

STATIC_NUMERIC_FEATURES = [
    "commute_minutes_one_way",
    "months_since_promotion"
]

STATIC_CATEGORICAL_FEATURES = [
    "department",
    "job_role"
]

TEMPORAL_FEATURES = [
    "job_satisfaction_score",
    "job_satisfaction_score_lag1",
    "job_satisfaction_score_delta1m",
    "job_satisfaction_score_slope3m",
    "work_life_balance_score",
    "work_life_balance_score_slope3m",
    "overtime_hours",
    "overtime_hours_delta1m",
    "overtime_hours_slope3m",
    "manager_support_score",
    "engagement_score",
    "stress_score",
    "absence_rate",
    "factor_deterioration_index"
]


def build_preprocessor(numeric_cols: list, categorical_cols: list) -> ColumnTransformer:
    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])
    
    cat_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="constant", fill_value="Unknown")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])
    
    return ColumnTransformer([
        ("num", num_pipeline, numeric_cols),
        ("cat", cat_pipeline, categorical_cols)
    ])


def classify_risk_tier(prob: float) -> str:
    if prob <= 0.25:
        return "Low"
    elif prob <= 0.50:
        return "Moderate"
    elif prob <= 0.75:
        return "High"
    else:
        return "Critical"


class AttritionPredictionEngine:
    def __init__(self, model_type: str = "xgboost"):
        self.model_type = model_type
        self.pipeline = None
        self.explainer = None
        self.feature_names = []

    def train(self, X_train: pd.DataFrame, y_train: pd.Series, numeric_cols: list, categorical_cols: list) -> dict[str, Any]:
        preprocessor = build_preprocessor(numeric_cols, categorical_cols)
        
        if self.model_type == "logistic_regression":
            clf = LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)
        elif self.model_type == "random_forest":
            clf = RandomForestClassifier(n_estimators=150, max_depth=6, class_weight="balanced", random_state=42)
        else: # xgboost
            clf = XGBClassifier(n_estimators=150, max_depth=4, learning_rate=0.08, eval_metric="logloss", random_state=42)
            
        self.pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("classifier", clf)
        ])
        
        self.pipeline.fit(X_train, y_train)
        
        # Fit SHAP explainer
        transformed_X = self.pipeline.named_steps["preprocessor"].transform(X_train)
        if self.model_type in ["random_forest", "xgboost"]:
            self.explainer = shap.TreeExplainer(self.pipeline.named_steps["classifier"])
        elif self.model_type == "logistic_regression":
            self.explainer = shap.LinearExplainer(self.pipeline.named_steps["classifier"], transformed_X)
            
        return {"status": "TRAINED", "model_type": self.model_type}

    def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series) -> dict[str, Any]:
        probs = self.pipeline.predict_proba(X_test)[:, 1]
        preds = (probs >= 0.40).astype(int) # Optimized cutoff
        
        return {
            "roc_auc": round(float(roc_auc_score(y_test, probs)), 4),
            "pr_auc": round(float(average_precision_score(y_test, probs)), 4),
            "precision": round(float(precision_score(y_test, preds, zero_division=0)), 4),
            "recall": round(float(recall_score(y_test, preds, zero_division=0)), 4),
            "f1_score": round(float(f1_score(y_test, preds, zero_division=0)), 4),
            "brier_score": round(float(brier_score_loss(y_test, probs)), 4),
            "confusion_matrix": confusion_matrix(y_test, preds).tolist()
        }

    def predict_single_with_explanation(self, single_row: pd.DataFrame, top_k: int = 4) -> dict[str, Any]:
        prob = float(self.pipeline.predict_proba(single_row)[0, 1])
        tier = classify_risk_tier(prob)
        
        explanations = []
        if self.explainer is not None:
            transformed = self.pipeline.named_steps["preprocessor"].transform(single_row)
            shap_values = self.explainer.shap_values(transformed)
            if isinstance(shap_values, list):
                sv = shap_values[1][0] if len(shap_values) > 1 else shap_values[0]
            elif len(shap_values.shape) > 1:
                sv = shap_values[0]
            else:
                sv = shap_values
                
            # Extract top features
            feature_names = self.pipeline.named_steps["preprocessor"].get_feature_names_out()
            top_indices = np.argsort(np.abs(sv))[::-1][:top_k]
            
            for idx in top_indices:
                feat_name = feature_names[idx].replace("num__", "").replace("cat__", "")
                explanations.append({
                    "feature": feat_name,
                    "shap_value": round(float(sv[idx]), 4),
                    "impact": "Increases Risk" if sv[idx] > 0 else "Decreases Risk"
                })
                
        return {
            "risk_probability": round(prob, 4),
            "risk_category": tier,
            "top_explanations": explanations
        }

    def save(self, filepath: str):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self, filepath)

    @classmethod
    def load(cls, filepath: str):
        return joblib.load(filepath)
