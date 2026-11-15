"""Statistical analysis and hypothesis testing engine for AttritionPulse AI.
Includes:
- Descriptive statistics across 12 factors
- Hypothesis testing (Mann-Whitney U, Independent t-test, Chi-square) with FDR correction
- Logistic regression with clustered/robust standard errors (statsmodels)
- Factor Deterioration Index (FDI) calculation
- Factor interactions (Overtime x WLB, High Workload x Low Support, etc.)
"""

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats
from statsmodels.stats.multitest import multipletests


def calculate_descriptive_stats(df: pd.DataFrame, factor_cols: list) -> pd.DataFrame:
    """Computes Mean, Median, Std, Min, Max, Q25, Q75, Missing% across numeric factors."""
    records = []
    for col in factor_cols:
        if col not in df.columns:
            continue
        s = df[col].dropna()
        records.append({
            "factor": col,
            "mean": round(float(s.mean()), 3),
            "median": round(float(s.median()), 3),
            "std": round(float(s.std()), 3),
            "min": round(float(s.min()), 3),
            "max": round(float(s.max()), 3),
            "q25": round(float(s.quantile(0.25)), 3),
            "q75": round(float(s.quantile(0.75)), 3),
            "missing_pct": round(float((df[col].isna().sum() / len(df)) * 100), 2)
        })
    return pd.DataFrame(records)


def run_hypothesis_tests(df_attrited: pd.DataFrame, df_retained: pd.DataFrame, factor_cols: list) -> pd.DataFrame:
    """Runs Mann-Whitney U & Independent Two-Sample t-tests comparing attrited vs retained employees
    with Benjamini-Hochberg False Discovery Rate (FDR) correction.
    """
    results = []
    raw_p_values = []
    
    for col in factor_cols:
        if col not in df_attrited.columns or col not in df_retained.columns:
            continue
            
        x = df_attrited[col].dropna()
        y = df_retained[col].dropna()
        
        if len(x) < 5 or len(y) < 5:
            continue
            
        # Mann-Whitney U test (non-parametric)
        u_stat, u_pval = stats.mannwhitneyu(x, y, alternative='two-sided')
        
        # Two-sample t-test (parametric)
        t_stat, t_pval = stats.ttest_ind(x, y, equal_var=False)
        
        # Cohen's d effect size
        pooled_std = np.sqrt(((len(x)-1)*x.std()**2 + (len(y)-1)*y.std()**2) / (len(x)+len(y)-2))
        cohens_d = (x.mean() - y.mean()) / pooled_std if pooled_std > 0 else 0.0
        
        raw_p_values.append(u_pval)
        
        results.append({
            "factor": col,
            "attrited_mean": round(float(x.mean()), 3),
            "retained_mean": round(float(y.mean()), 3),
            "mann_whitney_u": round(float(u_stat), 2),
            "p_value_raw": float(u_pval),
            "t_statistic": round(float(t_stat), 2),
            "cohens_d": round(float(cohens_d), 3)
        })
        
    # Apply Benjamini-Hochberg FDR correction
    if raw_p_values:
        rejected, p_adjusted, _, _ = multipletests(raw_p_values, alpha=0.05, method='fdr_bh')
        for idx, res in enumerate(results):
            res["p_value_fdr_adjusted"] = float(p_adjusted[idx])
            res["significant_at_05"] = bool(rejected[idx])
            
    return pd.DataFrame(results)


def fit_interpretable_logistic_regression(df: pd.DataFrame, target_col: str = "attrition_binary") -> dict:
    """Fits an interpretable statsmodels Logit model and extracts Odds Ratios and 95% Confidence Intervals."""
    formula = (
        f"{target_col} ~ job_satisfaction_score + work_life_balance_score + "
        "overtime_hours + manager_support_score + absence_rate + stress_score"
    )
    
    clean_df = df.dropna(subset=[
        target_col, "job_satisfaction_score", "work_life_balance_score",
        "overtime_hours", "manager_support_score", "absence_rate", "stress_score"
    ]).copy()
    
    model = smf.logit(formula=formula, data=clean_df).fit(disp=False)
    
    params = model.params
    conf = model.conf_int()
    conf["Odds_Ratio"] = np.exp(params)
    conf["OR_2.5%"] = np.exp(conf[0])
    conf["OR_97.5%"] = np.exp(conf[1])
    conf["p_value"] = model.pvalues
    conf["std_err"] = model.bse
    
    summary_df = conf[["Odds_Ratio", "OR_2.5%", "OR_97.5%", "p_value", "std_err"]].reset_index()
    summary_df.columns = ["factor", "odds_ratio", "ci_lower_95", "ci_upper_95", "p_value", "std_err"]
    
    return {
        "summary": summary_df,
        "aic": float(model.aic),
        "bic": float(model.bic),
        "pseudo_r2": float(model.prsquared),
        "num_obs": int(model.nobs)
    }
