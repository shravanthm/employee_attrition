"""Seed database with synthetic longitudinal employee records."""

import os
import sys
import pandas as pd
from datetime import datetime

# Add paths
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(base_dir, "backend"))
sys.path.insert(0, base_dir)

from app.db.session import engine, SessionLocal, Base
from app.models.entities import Employee, EmployeeMonthlySnapshot, AttritionEvent

def seed():
    print("Creating tables if not present...")
    Base.metadata.create_all(bind=engine)
    
    session = SessionLocal()
    try:
        emp_count = session.query(Employee).count()
        if emp_count > 0:
            print(f"Database already contains {emp_count} employees. Skipping seed.")
            return

        print("Loading synthetic CSVs...")
        emp_csv = os.path.join(base_dir, "data", "synthetic", "employees.csv")
        snap_csv = os.path.join(base_dir, "data", "synthetic", "monthly_snapshots.csv")
        event_csv = os.path.join(base_dir, "data", "synthetic", "attrition_events.csv")
        
        if not os.path.exists(emp_csv) or not os.path.exists(snap_csv):
            print("Synthetic CSV files not found!")
            return

        df_emp = pd.read_csv(emp_csv)
        df_snap = pd.read_csv(snap_csv)
        df_event = pd.read_csv(event_csv) if os.path.exists(event_csv) else None

        print(f"Inserting {len(df_emp)} employees...")
        employees = []
        for _, row in df_emp.iterrows():
            hire_d = datetime.strptime(str(row["hire_date"]), "%Y-%m-%d").date() if pd.notna(row["hire_date"]) else None
            emp = Employee(
                id=int(row["id"]),
                employee_code=str(row["employee_code"]),
                department=str(row["department"]),
                job_role=str(row["job_role"]),
                business_unit=str(row.get("business_unit", "Corporate")),
                location=str(row.get("location", "Headquarters")),
                hire_date=hire_d,
                employment_status=str(row.get("employment_status", "Active"))
            )
            employees.append(emp)
        session.bulk_save_objects(employees)
        session.commit()
        print("Employees inserted.")

        print(f"Inserting {len(df_snap)} monthly snapshots...")
        snapshots = []
        for _, row in df_snap.iterrows():
            snap_m = datetime.strptime(str(row["snapshot_month"]), "%Y-%m-%d").date()
            snap = EmployeeMonthlySnapshot(
                employee_id=int(row["employee_id"]),
                snapshot_month=snap_m,
                overtime_hours=float(row.get("overtime_hours", 0.0)),
                job_satisfaction_score=float(row["job_satisfaction_score"]) if pd.notna(row.get("job_satisfaction_score")) else None,
                work_life_balance_score=float(row["work_life_balance_score"]) if pd.notna(row.get("work_life_balance_score")) else None,
                manager_support_score=float(row["manager_support_score"]) if pd.notna(row.get("manager_support_score")) else None,
                engagement_score=float(row["engagement_score"]) if pd.notna(row.get("engagement_score")) else None,
                stress_score=float(row["stress_score"]) if pd.notna(row.get("stress_score")) else None,
                absence_rate=float(row.get("absence_rate", 0.0)),
                factor_deterioration_index=float(row["factor_deterioration_index"]) if pd.notna(row.get("factor_deterioration_index")) else None
            )
            snapshots.append(snap)
            if len(snapshots) >= 1000:
                session.bulk_save_objects(snapshots)
                session.commit()
                snapshots = []
        if snapshots:
            session.bulk_save_objects(snapshots)
            session.commit()
        print("Snapshots inserted.")

        if df_event is not None:
            print(f"Inserting {len(df_event)} attrition events...")
            events = []
            for _, row in df_event.iterrows():
                ev_d = datetime.strptime(str(row["event_date"]), "%Y-%m-%d").date() if pd.notna(row["event_date"]) else None
                end_d = datetime.strptime(str(row["observation_end_date"]), "%Y-%m-%d").date() if pd.notna(row["observation_end_date"]) else None
                ev = AttritionEvent(
                    employee_id=int(row["employee_id"]),
                    event_date=ev_d,
                    event_type=str(row.get("event_type", "Resignation")),
                    voluntary_flag=bool(row.get("voluntary_flag", True)),
                    reason_category=str(row.get("reason_category", "Career Change")),
                    observation_end_date=end_d,
                    censoring_status=int(row.get("censoring_status", 1))
                )
                events.append(ev)
            session.bulk_save_objects(events)
            session.commit()
            print("Attrition events inserted.")

        print("Database seeded successfully!")
    finally:
        session.close()

if __name__ == "__main__":
    seed()
