"""Auto-seeding utility to populate database on cold start if empty."""

import logging
import os
from datetime import datetime
import pandas as pd
from app.models.entities import Employee, EmployeeMonthlySnapshot, AttritionEvent
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def auto_seed_if_empty(db: Session):
    """Seed synthetic data if no employees exist in the database."""
    try:
        if db.query(Employee).count() > 0:
            return

        # Find synthetic dataset directory
        candidates = [
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "synthetic"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "data", "synthetic"),
            os.path.join(os.getcwd(), "data", "synthetic"),
            os.path.join(os.getcwd(), "backend", "data", "synthetic"),
        ]
        synth_dir = None
        for c in candidates:
            if os.path.exists(os.path.join(c, "employees.csv")):
                synth_dir = os.path.abspath(c)
                break

        if not synth_dir:
            logger.warning("Auto-seed skipped: synthetic dataset directory not found.")
            return

        emp_csv = os.path.join(synth_dir, "employees.csv")
        snap_csv = os.path.join(synth_dir, "monthly_snapshots.csv")
        event_csv = os.path.join(synth_dir, "attrition_events.csv")

        df_emp = pd.read_csv(emp_csv)
        df_snap = pd.read_csv(snap_csv)
        df_event = pd.read_csv(event_csv) if os.path.exists(event_csv) else None

        employees = []
        for _, row in df_emp.iterrows():
            hire_d = datetime.strptime(str(row["hire_date"]), "%Y-%m-%d").date() if pd.notna(row.get("hire_date")) else None
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
        db.bulk_save_objects(employees)
        db.commit()

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
        if snapshots:
            db.bulk_save_objects(snapshots)
            db.commit()

        if df_event is not None:
            events = []
            for _, row in df_event.iterrows():
                ev_d = datetime.strptime(str(row["event_date"]), "%Y-%m-%d").date() if pd.notna(row.get("event_date")) else None
                end_d = datetime.strptime(str(row["observation_end_date"]), "%Y-%m-%d").date() if pd.notna(row.get("observation_end_date")) else None
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
            if events:
                db.bulk_save_objects(events)
                db.commit()

        logger.info(f"Auto-seed completed: {len(employees)} employees, {len(snapshots)} snapshots.")
    except Exception as e:
        logger.warning(f"Auto-seed failed (non-fatal): {e}")
