# Data Dictionary — AttritionPulse AI Longitudinal Schema

**Schema Version:** 1.0.0  
**Entities:** Master Employee, Monthly Snapshots, Attrition Events  

---

## 1. Core Master Entity (`employees`)

| Field Name | Type | Description | Values / Range | Constraints |
|---|---|---|---|---|
| `id` | Integer | Auto-increment surrogate primary key | 1 .. N | Primary Key |
| `employee_code` | String(50) | Enterprise employee identifier | e.g. `EMP-0042` | Unique, Not Null |
| `department` | String(100) | Department assignment | Sales, R&D, HR | Not Null |
| `job_role` | String(100) | Job title / designation | Standardized role list | Not Null |
| `business_unit` | String(100) | Business operating unit | e.g. Enterprise, Consumer | Nullable |
| `location` | String(100) | Office location or geo region | e.g. London, Remote | Nullable |
| `employment_type` | String(50) | Nature of employment contract | Full-Time, Part-Time, Contractor | Default: Full-Time |
| `hire_date` | Date | Date of corporate onboarding | YYYY-MM-DD | Not Null |
| `employment_status` | String(50) | Current lifecycle status | Active, Terminated, On Leave | Default: Active |

---

## 2. Longitudinal Monthly Telemetry (`employee_monthly_snapshots`)

### Uniqueness Rule
Composite unique index: `(employee_id, snapshot_month)`. Exactly one observation record per employee per month.

### The Twelve Behavioral & Organizational Factors

| Factor # | Group Name | Fields | Description & Scale |
|---|---|---|---|
| **1** | Overtime & Workload | `overtime_hours`, `contracted_work_hours`, `overtime_ratio`, `workload_satisfaction` | Overtime hours beyond contracted schedule. Derived ratio: `(overtime_hours / contracted_hours) * 100`. Satisfaction: 1-5 scale. |
| **2** | Job Satisfaction | `job_satisfaction_score`, `satisfaction_change` | Survey score 1.0 - 5.0. Change compared to prior month. |
| **3** | Work-Life Balance | `work_life_balance_score`, `weekend_work_days`, `after_hours_work_days` | Rating 1.0 - 5.0. Frequency of weekend and off-hours engagements. |
| **4** | Career Progression | `months_since_promotion`, `promotion_in_period`, `career_growth_satisfaction` | Tenure in role, promotion occurrence, perceived growth trajectory (1-5). |
| **5** | Compensation Fairness | `salary_amount`, `bonus_amount`, `pay_fairness_score`, `benefits_satisfaction` | Annualized compensation, incentive payouts, and perceived equity (1-5). |
| **6** | Manager Support | `manager_support_score`, `one_to_one_meeting_count`, `manager_change_flag` | Manager efficacy rating (1-5), 1:1 cadence, and leadership disruption flag. |
| **7** | Employee Engagement | `engagement_score`, `motivation_score`, `meaningful_work_score` | Core engagement metrics on standard 1-5 Likert scale. |
| **8** | Work Environment | `work_environment_score`, `safety_score`, `psychological_safety_score` | Workplace climate and safety perceptions (1-5). |
| **9** | Attendance | `scheduled_work_days`, `absent_days`, `unplanned_absence_days`, `absence_rate` | Monthly attendance. Absence rate: `(absent_days / scheduled_days) * 100`. |
| **10** | Training & Development | `training_hours`, `skills_development_score`, `certification_count` | Skill enhancement hours and development satisfaction (1-5). |
| **11** | Travel & Commuting | `commute_minutes_one_way`, `monthly_commute_hours`, `business_travel_days` | Commute burden. Monthly commute hours: `(2 * commute_minutes * commute_days) / 60`. |
| **12** | Employee Wellbeing | `wellbeing_score`, `stress_score`, `exhaustion_score`, `recovery_score` | Voluntary, strictly confidential sentiment metrics (1-5). Never treated as clinical diagnostics. |

---

## 3. Ground Truth & Censoring Entity (`attrition_events`)

| Field Name | Type | Description | Values / Range | Constraints |
|---|---|---|---|---|
| `id` | Integer | Primary key | 1 .. N | Primary Key |
| `employee_id` | Integer | Foreign key to `employees.id` | Reference | Foreign Key, Not Null |
| `event_date` | Date | Date of departure or censoring cutoff | YYYY-MM-DD | Not Null |
| `event_type` | String(50) | Event categorization | Voluntary, Involuntary, Retirement, Censored | Not Null |
| `voluntary_flag` | Boolean | Primary event of interest flag | True for voluntary resignations | Not Null |
| `observation_end_date` | Date | End of follow-up observation window | YYYY-MM-DD | Not Null |
| `censoring_status` | Integer | Survival indicator | 1 = Event occurred, 0 = Censored (still active) | Not Null |
