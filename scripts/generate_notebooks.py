"""Script to generate all 8 Phase 3 exploratory data analysis notebooks in notebooks/."""

import os
import nbformat as nbf

NOTEBOOKS = [
    ("01_dataset_overview.ipynb", "01. Dataset Overview & Schema Inspection", 
     "import pandas as pd\nimport plotly.express as px\n\n# Load dataset\ndf_emps = pd.read_csv('../data/synthetic/employees.csv')\ndf_snaps = pd.read_csv('../data/synthetic/monthly_snapshots.csv')\nprint(f'Total employees: {len(df_emps)} | Total monthly snapshots: {len(df_snaps)}')\ndf_emps.head()"),
     
    ("02_data_quality_missingness.ipynb", "02. Data Quality & Missingness Analysis",
     "import pandas as pd\ndf_snaps = pd.read_csv('../data/synthetic/monthly_snapshots.csv')\nmissing = df_snaps.isnull().sum()\nprint('Missing values per column:\\n', missing[missing > 0])"),
     
    ("03_employee_distribution.ipynb", "03. Demographic & Departmental Distribution",
     "import pandas as pd\nimport plotly.express as px\ndf_emps = pd.read_csv('../data/synthetic/employees.csv')\nfig = px.pie(df_emps, names='department', title='Workforce Department Breakdown')\nfig.show()"),
     
    ("04_attrition_outcomes.ipynb", "04. Attrition Outcome Distribution & Right Censoring",
     "import pandas as pd\ndf_events = pd.read_csv('../data/synthetic/attrition_events.csv')\nprint(df_events['censoring_status'].value_counts())\nprint(df_events['event_type'].value_counts())"),
     
    ("05_twelve_factors.ipynb", "05. Twelve Behavioral & Organizational Factors EDA",
     "import pandas as pd\nimport plotly.express as px\ndf_snaps = pd.read_csv('../data/synthetic/monthly_snapshots.csv')\nfig = px.box(df_snaps, y='job_satisfaction_score', x='overtime_hours', title='Job Satisfaction vs Overtime')\nfig.show()"),
     
    ("06_missing_data_patterns.ipynb", "06. Missing Data Imputation & Sensitivity",
     "import pandas as pd\nfrom sklearn.impute import SimpleImputer\ndf_snaps = pd.read_csv('../data/synthetic/monthly_snapshots.csv')\nprint('Clean observation status:', df_snaps['data_quality_status'].value_counts())"),
     
    ("07_temporal_patterns_fdi.ipynb", "07. Longitudinal Trajectories & Factor Deterioration Index",
     "import pandas as pd\nimport sys\nsys.path.append('../backend')\nfrom app.analytics.temporal import engineer_temporal_features\ndf_snaps = pd.read_csv('../data/synthetic/monthly_snapshots.csv')\nfeatures = engineer_temporal_features(df_snaps)\nprint(features[['employee_id', 'factor_deterioration_index']].head())"),
     
    ("08_attrition_group_comparisons.ipynb", "08. Attrition Cohort Comparisons & Statistical Significance",
     "import pandas as pd\ndf_stats = pd.read_csv('../reports/hypothesis_tests.csv')\nprint('Significant factors with FDR correction:\\n', df_stats[df_stats['significant_at_05'] == True][['factor', 'cohens_d', 'p_value_fdr_adjusted']])")
]

def main():
    os.makedirs("notebooks", exist_ok=True)
    for filename, title, code in NOTEBOOKS:
        nb = nbf.v4.new_notebook()
        md_cell = nbf.v4.new_markdown_cell(f"# {title}\n\nAttritionPulse AI — Exploratory Research Notebook.")
        code_cell = nbf.v4.new_code_cell(code)
        nb['cells'] = [md_cell, code_cell]
        filepath = os.path.join("notebooks", filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)
        print(f"✅ Generated notebook: {filepath}")

if __name__ == "__main__":
    main()
