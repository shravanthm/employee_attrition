"""Tests for Phase 1 Database Foundation."""

import os
import pytest
from datetime import date, datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from app.db.session import Base
from app.models.entities import (
    Role, User, Employee, EmployeeMonthlySnapshot, AttritionEvent,
    RiskPrediction, PredictionExplanation, Intervention, InterventionOutcome,
    ModelRegistry, DataImportJob, AuditLog
)
from app.core.security import hash_password, verify_password
from app.core.config import settings

TEST_DB_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db_session():
    test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=test_engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)


def test_environment_and_config():
    assert settings.POSTGRES_DB == "attritionpulse"
    assert settings.POSTGRES_PORT == 5432
    assert "http://localhost:5173" in settings.CORS_ORIGINS


def test_argon2_password_hashing():
    raw_pass = "EnterpriseSecurePass2026!"
    hashed = hash_password(raw_pass)
    assert hashed != raw_pass
    assert verify_password(raw_pass, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False


def test_role_and_user_creation(db_session):
    role = Role(role_name="HR_ADMIN", permissions=["view_all", "export_data", "predict"])
    db_session.add(role)
    db_session.commit()
    db_session.refresh(role)
    assert role.id is not None

    user = User(
        username="hr_director",
        email="director@company.com",
        password_hash=hash_password("admin_pass"),
        role_id=role.id,
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.id is not None
    assert user.role.role_name == "HR_ADMIN"


def test_employee_and_snapshot_creation(db_session):
    emp = Employee(
        employee_code="EMP-1001",
        department="Sales",
        job_role="Sales Executive",
        business_unit="Enterprise",
        location="North America",
        hire_date=date(2022, 1, 15),
        employment_status="Active"
    )
    db_session.add(emp)
    db_session.commit()
    db_session.refresh(emp)
    assert emp.id is not None

    # Add snapshot
    snap = EmployeeMonthlySnapshot(
        employee_id=emp.id,
        snapshot_month=date(2026, 1, 1),
        overtime_hours=15.0,
        job_satisfaction_score=4.0,
        work_life_balance_score=3.5,
        salary_amount=75000.0,
        manager_support_score=4.2,
        engagement_score=4.0,
        work_environment_score=4.0,
        scheduled_work_days=20,
        absent_days=1,
        training_hours=8.0,
        business_travel_days=2,
        wellbeing_score=3.8
    )
    db_session.add(snap)
    db_session.commit()
    db_session.refresh(snap)

    assert snap.id is not None
    assert snap.employee.employee_code == "EMP-1001"


def test_snapshot_unique_constraint(db_session):
    emp = Employee(
        employee_code="EMP-1002",
        department="Engineering",
        job_role="Software Engineer",
        hire_date=date(2023, 6, 1),
        employment_status="Active"
    )
    db_session.add(emp)
    db_session.commit()

    snap1 = EmployeeMonthlySnapshot(
        employee_id=emp.id,
        snapshot_month=date(2026, 1, 1),
        overtime_hours=10.0
    )
    db_session.add(snap1)
    db_session.commit()

    # Second snapshot for same employee and same month must fail unique constraint
    snap2 = EmployeeMonthlySnapshot(
        employee_id=emp.id,
        snapshot_month=date(2026, 1, 1),
        overtime_hours=20.0
    )
    db_session.add(snap2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_attrition_event_and_prediction(db_session):
    emp = Employee(
        employee_code="EMP-1003",
        department="HR",
        job_role="HR Specialist",
        hire_date=date(2021, 3, 1),
        employment_status="Terminated"
    )
    db_session.add(emp)
    db_session.commit()

    event = AttritionEvent(
        employee_id=emp.id,
        event_date=date(2026, 3, 31),
        event_type="Voluntary",
        voluntary_flag=True,
        reason_category="Better Offer",
        observation_end_date=date(2026, 3, 31),
        censoring_status=1
    )
    db_session.add(event)

    model = ModelRegistry(
        model_name="xgboost_attrition_classifier",
        model_version="v1.0.0",
        model_type="Classifier",
        dataset_version="ibm_synthetic_longitudinal_v1",
        metrics={"roc_auc": 0.88, "f1_score": 0.74},
        artifact_location="models/xgb_v1.pkl",
        status="ACTIVE"
    )
    db_session.add(model)
    db_session.commit()

    pred = RiskPrediction(
        employee_id=emp.id,
        model_id=model.id,
        cutoff_date=date(2026, 3, 1),
        prediction_horizon_days=90,
        risk_probability=0.78,
        risk_category="High",
        model_version="v1.0.0"
    )
    db_session.add(pred)
    db_session.commit()

    explanation = PredictionExplanation(
        prediction_id=pred.id,
        feature_name="overtime_hours",
        feature_value=35.0,
        shap_value=0.28,
        explanation_metadata={"impact": "High positive contribution to flight risk"}
    )
    db_session.add(explanation)
    db_session.commit()

    assert pred.id is not None
    assert len(pred.explanations) == 1
    assert pred.explanations[0].shap_value == 0.28
