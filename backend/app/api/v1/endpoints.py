"""FastAPI v1 endpoints for AttritionPulse AI."""


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
from fastapi import APIRouter, Depends, HTTPException, Query
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
