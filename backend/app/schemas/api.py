"""Pydantic V2 request & response schemas for AttritionPulse AI API."""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import date, datetime


# Token & Auth
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    role_name: Optional[str] = None


# Employee
class EmployeeResponse(BaseModel):
    id: int
    employee_code: str
    department: str
    job_role: str
    business_unit: Optional[str] = None
    location: Optional[str] = None
    hire_date: date
    employment_status: str

    class Config:
        from_attributes = True


# Monthly Snapshot
class SnapshotResponse(BaseModel):
    id: int
    employee_id: int
    snapshot_month: date
    overtime_hours: float
    job_satisfaction_score: Optional[float]
    work_life_balance_score: Optional[float]
    manager_support_score: Optional[float]
    engagement_score: Optional[float]
    stress_score: Optional[float]
    absence_rate: float
    factor_deterioration_index: Optional[float]

    class Config:
        from_attributes = True


# Prediction
class ExplanationItem(BaseModel):
    feature: str
    shap_value: float
    impact: str


class PredictionResponse(BaseModel):
    employee_id: int
    risk_probability: float
    risk_category: str
    prediction_horizon_days: int = 90
    top_explanations: List[ExplanationItem]


# Survival
class SurvivalHorizonPoint(BaseModel):
    horizon_days: int
    survival_probability: float
    cumulative_attrition_risk: float


class SurvivalResponse(BaseModel):
    employee_id: int
    median_survival_days: Optional[float] = None
    survival_timeline: List[SurvivalHorizonPoint]


# Dashboard Overview
class DashboardMetrics(BaseModel):
    total_employees: int
    active_employees: int
    high_risk_count: int
    moderate_risk_count: int
    low_risk_count: int
    average_fdi: float
    department_distribution: Dict[str, int]
