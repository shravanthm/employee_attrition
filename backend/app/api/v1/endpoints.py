"""FastAPI v1 endpoints for AttritionPulse AI."""


import datetime
import io
import os
import pandas as pd
from app.analytics.temporal import engineer_temporal_features
from app.db.session import get_db
from app.models.entities import Employee, EmployeeMonthlySnapshot
from app.schemas.api import (
    DashboardMetrics,
    EmployeeResponse,
    PredictionResponse,
    SnapshotResponse,
    SurvivalResponse,
)
from app.services.analytics_service import AnalyticsService
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v1")


@router.get("/metrics/dashboard", response_model=DashboardMetrics, tags=["Dashboard"])
def get_dashboard_metrics(db: Session = Depends(get_db)):
    """Retrieve overall workforce attrition metrics and risk distribution."""
    return AnalyticsService.get_dashboard_metrics(db)


@router.get("/employees", response_model=list[EmployeeResponse], tags=["Employees"])
def list_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    department: str = None,
    db: Session = Depends(get_db)
):
    """Retrieve paginated list of employees with optional department filter."""
    query = db.query(Employee)
    if department:
        query = query.filter(Employee.department == department)
    return query.offset(skip).limit(limit).all()


@router.get("/employees/{employee_id}", response_model=EmployeeResponse, tags=["Employees"])
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    """Retrieve single employee master profile."""
    emp = db.query(Employee).filter(Employee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


@router.get("/employees/{employee_id}/snapshots", response_model=list[SnapshotResponse], tags=["Employees"])
def get_employee_snapshots(employee_id: int, db: Session = Depends(get_db)):
    """Retrieve longitudinal 12-factor telemetry snapshots for employee."""
    snapshots = db.query(EmployeeMonthlySnapshot).filter(
        EmployeeMonthlySnapshot.employee_id == employee_id
    ).order_by(EmployeeMonthlySnapshot.snapshot_month.asc()).all()
    return snapshots


@router.post("/predictions/{employee_id}", response_model=PredictionResponse, tags=["Predictions"])
def predict_employee_attrition(employee_id: int, db: Session = Depends(get_db)):
    """Predict 90-day attrition probability with SHAP explanation."""
    try:
        return AnalyticsService.predict_employee_risk(employee_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/survival/{employee_id}", response_model=SurvivalResponse, tags=["Survival Analysis"])
def get_employee_survival(employee_id: int, db: Session = Depends(get_db)):
    """Generate multi-horizon survival probability curve using Cox PH."""
    try:
        return AnalyticsService.get_employee_survival_timeline(employee_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/employees/upload-csv", tags=["Data Ingestion"])
async def upload_employees_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload and ingest employee records and longitudinal monthly snapshots."""
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        df.columns = [c.strip() for c in df.columns]

        # Check required columns
        req_cols = ["employee_code", "snapshot_month", "department", "job_role"]
        missing = [c for c in req_cols if c not in df.columns]
        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required columns in CSV: {', '.join(missing)}. "
                       f"Expected longitudinal format with: {', '.join(req_cols)}."
            )

        # Impute missing values per employee (forward fill, backward fill, then neutral default)
        score_cols = [
            "job_satisfaction_score", "work_life_balance_score",
            "manager_support_score", "engagement_score", "stress_score"
        ]
        for col in score_cols:
            if col in df.columns:
                df[col] = df.groupby("employee_code")[col].transform(lambda s: s.ffill().bfill().fillna(3.0))

        if "overtime_hours" in df.columns:
            df["overtime_hours"] = df["overtime_hours"].fillna(0.0)
        if "absence_rate" in df.columns:
            df["absence_rate"] = df["absence_rate"].fillna(0.0)

        unique_codes = df["employee_code"].unique()
        emp_map = {}

        for code in unique_codes:
            emp = db.query(Employee).filter(Employee.employee_code == str(code)).first()
            emp_rows = df[df["employee_code"] == code]
            first_row = emp_rows.iloc[0]

            hire_d = datetime.date(2023, 1, 1)
            if "hire_date" in df.columns and pd.notna(first_row.get("hire_date")):
                try:
                    hire_d = datetime.datetime.strptime(str(first_row["hire_date"])[:10], "%Y-%m-%d").date()
                except Exception:
                    pass

            dept = str(first_row.get("department", "General"))
            role = str(first_row.get("job_role", "Specialist"))
            status = str(first_row.get("employment_status", "Active"))

            if not emp:
                emp = Employee(
                    employee_code=str(code),
                    department=dept,
                    job_role=role,
                    hire_date=hire_d,
                    employment_status=status,
                    business_unit="Enterprise",
                    location="Headquarters"
                )
                db.add(emp)
                db.flush()
            else:
                emp.department = dept
                emp.job_role = role
                emp.employment_status = status
            emp_map[str(code)] = emp.id

        # Ingest monthly snapshots
        snapshots_count = 0
        for _, row in df.iterrows():
            emp_id = emp_map[str(row["employee_code"])]
            snap_m = datetime.datetime.strptime(str(row["snapshot_month"])[:10], "%Y-%m-%d").date()

            snap = db.query(EmployeeMonthlySnapshot).filter(
                EmployeeMonthlySnapshot.employee_id == emp_id,
                EmployeeMonthlySnapshot.snapshot_month == snap_m
            ).first()

            ot = float(row.get("overtime_hours", 0.0)) if pd.notna(row.get("overtime_hours")) else 0.0
            js = float(row.get("job_satisfaction_score", 3.0)) if pd.notna(row.get("job_satisfaction_score")) else 3.0
            wlb = float(row.get("work_life_balance_score", 3.0)) if pd.notna(row.get("work_life_balance_score")) else 3.0
            ms = float(row.get("manager_support_score", 3.0)) if pd.notna(row.get("manager_support_score")) else 3.0
            eng = float(row.get("engagement_score", 3.0)) if pd.notna(row.get("engagement_score")) else 3.0
            stress = float(row.get("stress_score", 2.0)) if pd.notna(row.get("stress_score")) else 2.0
            absence = float(row.get("absence_rate", 0.0)) if pd.notna(row.get("absence_rate")) else 0.0

            if snap:
                snap.overtime_hours = ot
                snap.job_satisfaction_score = js
                snap.work_life_balance_score = wlb
                snap.manager_support_score = ms
                snap.engagement_score = eng
                snap.stress_score = stress
                snap.absence_rate = absence
            else:
                snap = EmployeeMonthlySnapshot(
                    employee_id=emp_id,
                    snapshot_month=snap_m,
                    overtime_hours=ot,
                    job_satisfaction_score=js,
                    work_life_balance_score=wlb,
                    manager_support_score=ms,
                    engagement_score=eng,
                    stress_score=stress,
                    absence_rate=absence
                )
                db.add(snap)
            snapshots_count += 1

        db.commit()

        # Compute and persist Factor Deterioration Index (FDI) for ingested employees
        for emp_id in emp_map.values():
            snaps = db.query(EmployeeMonthlySnapshot).filter(
                EmployeeMonthlySnapshot.employee_id == emp_id
            ).order_by(EmployeeMonthlySnapshot.snapshot_month.asc()).all()

            if len(snaps) >= 2:
                snap_records = [{
                    "employee_id": s.employee_id,
                    "snapshot_month": s.snapshot_month,
                    "overtime_hours": s.overtime_hours,
                    "job_satisfaction_score": s.job_satisfaction_score,
                    "work_life_balance_score": s.work_life_balance_score,
                    "manager_support_score": s.manager_support_score,
                    "engagement_score": s.engagement_score,
                    "stress_score": s.stress_score,
                    "absence_rate": s.absence_rate
                } for s in snaps]
                df_temp = engineer_temporal_features(pd.DataFrame(snap_records))
                if not df_temp.empty and "factor_deterioration_index" in df_temp.columns:
                    latest_fdi = float(df_temp.iloc[-1]["factor_deterioration_index"])
                    snaps[-1].factor_deterioration_index = latest_fdi

        db.commit()

        return {
            "status": "success",
            "message": f"Successfully ingested {len(unique_codes)} employees and {snapshots_count} monthly snapshots.",
            "employees_count": len(unique_codes),
            "snapshots_count": snapshots_count
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to process CSV: {str(e)}")


def _get_reports_dir():
    # Resolve repository root reports folder
    p = os.path.abspath(__file__)
    for _ in range(5):
        p = os.path.dirname(p)
    rep_path = os.path.join(p, "reports")
    if os.path.exists(rep_path):
        return rep_path
    alt_path = os.path.join(os.getcwd(), "reports")
    if os.path.exists(alt_path):
        return alt_path
    return rep_path


@router.get("/reports/data", tags=["Reports"])
def get_reports_data():
    """Retrieve structured research analysis tables, hypothesis tests, model benchmarks, and survival data."""
    try:
        rep_dir = _get_reports_dir()

        def read_csv_safe(filename):
            path = os.path.join(rep_dir, filename)
            if os.path.exists(path):
                df = pd.read_csv(path)
                return df.where(pd.notnull(df), None).to_dict(orient="records")
            return []

        def read_text_safe(filename):
            path = os.path.join(rep_dir, filename)
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    return f.read()
            return ""

        return {
            "hypothesis_tests": read_csv_safe("hypothesis_tests.csv"),
            "ml_evaluations": read_csv_safe("ml_model_evaluation.csv"),
            "cox_hazard_ratios": read_csv_safe("cox_hazard_ratios.csv"),
            "descriptive_statistics": read_csv_safe("descriptive_statistics.csv"),
            "logistic_regression": read_csv_safe("logistic_regression_odds_ratios.csv"),
            "methodology_markdown": read_text_safe("statistical_analysis_report.md")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load research reports: {str(e)}")


@router.get("/reports/download/{filename}", tags=["Reports"])
def download_report_file(filename: str):
    """Download research CSV dataset or markdown summary."""
    allowed = [
        "hypothesis_tests.csv",
        "ml_model_evaluation.csv",
        "cox_hazard_ratios.csv",
        "descriptive_statistics.csv",
        "logistic_regression_odds_ratios.csv",
        "statistical_analysis_report.md"
    ]
    if filename not in allowed:
        raise HTTPException(status_code=400, detail="File not authorized for download")
    rep_dir = _get_reports_dir()
    path = os.path.join(rep_dir, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Report file not found")
    return FileResponse(path, filename=filename, media_type="application/octet-stream")


