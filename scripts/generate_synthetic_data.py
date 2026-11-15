"""Synthetic Longitudinal Data Generator for AttritionPulse AI.
Simulates monthly employee snapshots across all 12 factors with temporal trends and attrition events.
"""

import os
import argparse
import datetime
import numpy as np
import pandas as pd


DEPARTMENTS = ["Sales", "Research & Development", "Human Resources"]
JOB_ROLES = {
    "Sales": ["Sales Executive", "Sales Representative", "Manager"],
    "Research & Development": ["Research Scientist", "Laboratory Technician", "Manufacturing Director", "Healthcare Representative", "Manager"],
    "Human Resources": ["Human Resources", "Manager"]
}

def generate_synthetic_data(num_employees=200, num_months=12, start_date_str="2025-01-01", seed=42):
    np.random.seed(seed)
    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
    
    employees = []
    snapshots = []
    attrition_events = []
    
    for i in range(1, num_employees + 1):
        emp_code = f"EMP-{i:04d}"
        dept = np.random.choice(DEPARTMENTS, p=[0.3, 0.6, 0.1])
        role = np.random.choice(JOB_ROLES[dept])
        hire_offset = np.random.randint(300, 3000)
        hire_date = start_date - datetime.timedelta(days=hire_offset)
        
        # Base employee propensity to attrite (latent flight risk)
        base_flight_risk = np.random.beta(2, 5) # average around 0.28
        base_salary = np.random.normal(65000, 15000)
        
        emp_record = {
            "id": i,
            "employee_code": emp_code,
            "department": dept,
            "job_role": role,
            "hire_date": hire_date.isoformat(),
            "employment_status": "Active"
        }
        
        has_left = False
        departure_month_idx = None
        
        # Simulate monthly trajectory
        current_job_sat = np.random.uniform(2.5, 4.5)
        current_wlb = np.random.uniform(2.5, 4.5)
        current_engagement = np.random.uniform(2.8, 4.5)
        current_overtime = np.random.exponential(8)
        
        for m in range(num_months):
            if has_left:
                break
                
            # Month start date
            snap_month = (datetime.datetime(start_date.year, start_date.month, 1) + pd.DateOffset(months=m)).date()
            
            # If latent flight risk is high, factors deteriorate over time
            if base_flight_risk > 0.4:
                current_overtime += np.random.normal(3.0, 2.0)
                current_job_sat = max(1.0, current_job_sat - np.random.uniform(0.1, 0.35))
                current_wlb = max(1.0, current_wlb - np.random.uniform(0.1, 0.35))
                current_engagement = max(1.0, current_engagement - np.random.uniform(0.1, 0.3))
            else:
                current_overtime = max(0.0, current_overtime + np.random.normal(0, 1.5))
                current_job_sat = np.clip(current_job_sat + np.random.normal(0, 0.1), 1.0, 5.0)
                current_wlb = np.clip(current_wlb + np.random.normal(0, 0.1), 1.0, 5.0)
                current_engagement = np.clip(current_engagement + np.random.normal(0, 0.1), 1.0, 5.0)

            contracted_hours = 160.0
            actual_ot = max(0.0, current_overtime)
            ot_ratio = round((actual_ot / contracted_hours) * 100, 2)
            
            # Attendance
            scheduled_days = 20
            absent_days = int(np.random.poisson(1.0 + (5.0 - current_job_sat) * 0.4))
            absence_rate = round((absent_days / scheduled_days) * 100, 2)
            
            # Commute
            commute_mins = np.random.choice([15, 30, 45, 60, 90], p=[0.2, 0.4, 0.2, 0.15, 0.05])
            monthly_commute = round(2.0 * commute_mins * 20 / 60.0, 1)
            
            snapshot = {
                "employee_id": i,
                "snapshot_month": snap_month.isoformat(),
                # Factor 1: Overtime & Workload
                "overtime_hours": round(actual_ot, 1),
                "overtime_days": int(actual_ot // 3),
                "contracted_work_hours": contracted_hours,
                "total_work_hours": round(contracted_hours + actual_ot, 1),
                "workload_satisfaction": round(np.clip(current_wlb + np.random.normal(0, 0.2), 1.0, 5.0), 2),
                "overtime_ratio": ot_ratio,
                # Factor 2: Job Satisfaction
                "job_satisfaction_score": round(current_job_sat, 2),
                "satisfaction_change": round(np.random.normal(0, 0.15), 2),
                # Factor 3: Work-Life Balance
                "work_life_balance_score": round(current_wlb, 2),
                "weekend_work_days": int(actual_ot // 8),
                "after_hours_work_days": int(actual_ot // 4),
                # Factor 4: Career Progression
                "months_since_promotion": int(np.random.uniform(2, 48)),
                "promotion_in_period": False,
                "career_growth_satisfaction": round(np.clip(current_job_sat * 0.9, 1.0, 5.0), 2),
                # Factor 5: Compensation Fairness
                "salary_amount": round(base_salary, 2),
                "bonus_amount": round(base_salary * 0.08, 2),
                "pay_fairness_score": round(np.clip(current_job_sat * 0.95, 1.0, 5.0), 2),
                # Factor 6: Manager Support
                "manager_support_score": round(np.clip(4.0 - (base_flight_risk * 1.5) + np.random.normal(0, 0.2), 1.0, 5.0), 2),
                "one_to_one_meeting_count": int(np.random.poisson(2)),
                # Factor 7: Employee Engagement
                "engagement_score": round(current_engagement, 2),
                "motivation_score": round(np.clip(current_engagement + np.random.normal(0, 0.1), 1.0, 5.0), 2),
                # Factor 8: Work Environment
                "work_environment_score": round(np.random.uniform(3.0, 4.8), 2),
                # Factor 9: Attendance
                "scheduled_work_days": scheduled_days,
                "absent_days": absent_days,
                "absence_rate": absence_rate,
                # Factor 10: Training & Development
                "training_hours": round(np.random.exponential(3.0), 1),
                # Factor 11: Travel & Commuting
                "commute_minutes_one_way": commute_mins,
                "monthly_commute_hours": monthly_commute,
                "business_travel_days": int(np.random.poisson(1)),
                # Factor 12: Employee Wellbeing
                "wellbeing_score": round(np.clip(current_wlb * 0.95, 1.0, 5.0), 2),
                "stress_score": round(np.clip(1.0 + (actual_ot / 15.0), 1.0, 5.0), 2),
                "data_quality_status": "VALID"
            }
            snapshots.append(snapshot)
            
            # Attrition condition: high latent risk + deteriorating conditions in months 6-12
            monthly_leave_prob = 0.02 + (0.35 if (current_job_sat < 2.0 and actual_ot > 20.0) else (base_flight_risk * 0.08))
            if m >= 3 and np.random.rand() < monthly_leave_prob:
                has_left = True
                emp_record["employment_status"] = "Terminated"
                attrition_events.append({
                    "employee_id": i,
                    "event_date": snap_month.isoformat(),
                    "event_type": "Voluntary",
                    "voluntary_flag": True,
                    "reason_category": "Workload & Dissatisfaction",
                    "verified_status": "VERIFIED",
                    "observation_end_date": snap_month.isoformat(),
                    "censoring_status": 1
                })
        
        # If employee did not leave, record censored observation end date
        if not has_left:
            last_month = (datetime.datetime(start_date.year, start_date.month, 1) + pd.DateOffset(months=num_months - 1)).date()
            attrition_events.append({
                "employee_id": i,
                "event_date": last_month.isoformat(),
                "event_type": "Censored",
                "voluntary_flag": False,
                "reason_category": "Active At End of Study",
                "verified_status": "VERIFIED",
                "observation_end_date": last_month.isoformat(),
                "censoring_status": 0
            })
            
        employees.append(emp_record)
        
    os.makedirs("data/synthetic", exist_ok=True)
    pd.DataFrame(employees).to_csv("data/synthetic/employees.csv", index=False)
    pd.DataFrame(snapshots).to_csv("data/synthetic/monthly_snapshots.csv", index=False)
    pd.DataFrame(attrition_events).to_csv("data/synthetic/attrition_events.csv", index=False)
    
    print(f"✅ Generated {len(employees)} employees, {len(snapshots)} monthly snapshots, {len(attrition_events)} events.")
    return len(employees), len(snapshots), len(attrition_events)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--employees", type=int, default=300)
    parser.add_argument("--months", type=int, default=12)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    
    generate_synthetic_data(num_employees=args.employees, num_months=args.months, seed=args.seed)
