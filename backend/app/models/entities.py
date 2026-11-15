"""Complete SQLAlchemy 2.0 ORM Models for AttritionPulse AI.
Includes:
- employees
- employee_monthly_snapshots (12 attrition factors + longitudinal measurements)
- attrition_events
- users
- roles
- interventions
- intervention_outcomes
- risk_predictions
- prediction_explanations
- model_registry
- data_import_jobs
- audit_logs
"""

import datetime

from app.db.session import Base
from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship


def utcnow():
    return datetime.datetime.now(datetime.UTC)


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(50), unique=True, nullable=False)
    permissions = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    role = relationship("Role", back_populates="users")
    audit_logs = relationship("AuditLog", back_populates="user")


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50), unique=True, nullable=False, index=True)
    department = Column(String(100), nullable=False, index=True)
    job_role = Column(String(100), nullable=False, index=True)
    business_unit = Column(String(100), nullable=True)
    location = Column(String(100), nullable=True)
    employment_type = Column(String(50), default="Full-Time", nullable=False)
    hire_date = Column(Date, nullable=False)
    manager_reference = Column(String(50), nullable=True)
    employment_status = Column(String(50), default="Active", nullable=False, index=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    # Relationships
    snapshots = relationship("EmployeeMonthlySnapshot", back_populates="employee", cascade="all, delete-orphan")
    attrition_events = relationship("AttritionEvent", back_populates="employee", cascade="all, delete-orphan")
    predictions = relationship("RiskPrediction", back_populates="employee", cascade="all, delete-orphan")
    interventions = relationship("Intervention", back_populates="employee", cascade="all, delete-orphan")


class EmployeeMonthlySnapshot(Base):
    __tablename__ = "employee_monthly_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    snapshot_month = Column(Date, nullable=False, index=True)

    # Factor 1: Overtime & Workload
    overtime_hours = Column(Float, default=0.0)
    overtime_days = Column(Integer, default=0)
    contracted_work_hours = Column(Float, default=160.0)
    total_work_hours = Column(Float, default=160.0)
    workload_satisfaction = Column(Float, nullable=True)  # 1-5 scale
    overtime_ratio = Column(Float, default=0.0)  # Derived: overtime_hours / contracted_work_hours * 100

    # Factor 2: Job Satisfaction
    job_satisfaction_score = Column(Float, nullable=True)  # 1-5 scale
    satisfaction_change = Column(Float, default=0.0)
    satisfaction_survey_date = Column(Date, nullable=True)

    # Factor 3: Work-Life Balance
    work_life_balance_score = Column(Float, nullable=True)  # 1-5 scale
    weekend_work_days = Column(Integer, default=0)
    after_hours_work_days = Column(Integer, default=0)
    schedule_change_count = Column(Integer, default=0)
    flexible_work_days = Column(Integer, default=0)

    # Factor 4: Career Progression
    months_since_promotion = Column(Integer, default=0)
    promotion_in_period = Column(Boolean, default=False)
    internal_transfer_count = Column(Integer, default=0)
    career_growth_satisfaction = Column(Float, nullable=True)
    development_opportunity_score = Column(Float, nullable=True)

    # Factor 5: Compensation Fairness
    salary_amount = Column(Float, nullable=True)
    salary_currency = Column(String(10), default="USD")
    bonus_amount = Column(Float, default=0.0)
    salary_change_percentage = Column(Float, default=0.0)
    pay_fairness_score = Column(Float, nullable=True)
    benefits_satisfaction = Column(Float, nullable=True)

    # Factor 6: Manager Support
    manager_support_score = Column(Float, nullable=True)
    communication_score = Column(Float, nullable=True)
    feedback_score = Column(Float, nullable=True)
    recognition_count = Column(Integer, default=0)
    one_to_one_meeting_count = Column(Integer, default=0)
    manager_change_flag = Column(Boolean, default=False)

    # Factor 7: Employee Engagement
    engagement_score = Column(Float, nullable=True)
    motivation_score = Column(Float, nullable=True)
    commitment_score = Column(Float, nullable=True)
    meaningful_work_score = Column(Float, nullable=True)

    # Factor 8: Work Environment
    work_environment_score = Column(Float, nullable=True)
    safety_score = Column(Float, nullable=True)
    resources_score = Column(Float, nullable=True)
    collaboration_score = Column(Float, nullable=True)
    psychological_safety_score = Column(Float, nullable=True)

    # Factor 9: Attendance
    scheduled_work_days = Column(Integer, default=20)
    absent_days = Column(Integer, default=0)
    unplanned_absence_days = Column(Integer, default=0)
    late_arrival_count = Column(Integer, default=0)
    leave_days = Column(Integer, default=0)
    absence_rate = Column(Float, default=0.0)

    # Factor 10: Training & Development
    training_hours = Column(Float, default=0.0)
    training_sessions = Column(Integer, default=0)
    training_relevance_score = Column(Float, nullable=True)
    skills_development_score = Column(Float, nullable=True)
    development_plan_flag = Column(Boolean, default=False)
    certification_count = Column(Integer, default=0)

    # Factor 11: Travel & Commuting
    business_travel_days = Column(Integer, default=0)
    business_travel_nights = Column(Integer, default=0)
    commute_minutes_one_way = Column(Float, default=30.0)
    commute_days = Column(Integer, default=20)
    remote_work_days = Column(Integer, default=0)
    travel_burden_score = Column(Float, nullable=True)
    monthly_commute_hours = Column(Float, default=20.0)

    # Factor 12: Employee Wellbeing (Sensitive voluntary data)
    wellbeing_score = Column(Float, nullable=True)
    stress_score = Column(Float, nullable=True)
    exhaustion_score = Column(Float, nullable=True)
    belonging_score = Column(Float, nullable=True)
    recovery_score = Column(Float, nullable=True)

    # Temporal feature calculations
    factor_deterioration_index = Column(Float, nullable=True)

    # Data Quality & Missingness Tracking
    source_metadata = Column(JSON, nullable=True)
    missingness_indicators = Column(JSON, nullable=True)
    data_quality_status = Column(String(50), default="VALID", nullable=False)

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("employee_id", "snapshot_month", name="uq_emp_snapshot_month"),
        Index("ix_snapshot_emp_month", "employee_id", "snapshot_month"),
    )

    employee = relationship("Employee", back_populates="snapshots")


class AttritionEvent(Base):
    __tablename__ = "attrition_events"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    event_date = Column(Date, nullable=False)
    event_type = Column(String(50), nullable=False)  # Voluntary, Involuntary, Retirement, Transfer
    voluntary_flag = Column(Boolean, default=True, nullable=False)
    reason_category = Column(String(100), nullable=True)
    verified_status = Column(String(50), default="VERIFIED", nullable=False)
    observation_end_date = Column(Date, nullable=False)
    censoring_status = Column(Integer, default=1, nullable=False)  # 1 = Event occurred, 0 = Censored

    employee = relationship("Employee", back_populates="attrition_events")


class ModelRegistry(Base):
    __tablename__ = "model_registry"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(100), nullable=False)
    model_version = Column(String(50), nullable=False)
    model_type = Column(String(50), nullable=False)  # Classifier, Survival, SHAP
    training_date = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    dataset_version = Column(String(100), nullable=False)
    metrics = Column(JSON, nullable=False, default=dict)
    artifact_location = Column(String(255), nullable=False)
    status = Column(String(50), default="ACTIVE", nullable=False)

    predictions = relationship("RiskPrediction", back_populates="model")


class RiskPrediction(Base):
    __tablename__ = "risk_predictions"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    model_id = Column(Integer, ForeignKey("model_registry.id", ondelete="SET NULL"), nullable=True)
    prediction_date = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    cutoff_date = Column(Date, nullable=False)
    prediction_horizon_days = Column(Integer, default=90, nullable=False)
    risk_probability = Column(Float, nullable=False)
    risk_category = Column(String(50), nullable=False)  # Low, Moderate, High, Critical
    model_version = Column(String(50), nullable=False)

    employee = relationship("Employee", back_populates="predictions")
    model = relationship("ModelRegistry", back_populates="predictions")
    explanations = relationship("PredictionExplanation", back_populates="prediction", cascade="all, delete-orphan")


class PredictionExplanation(Base):
    __tablename__ = "prediction_explanations"

    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(Integer, ForeignKey("risk_predictions.id", ondelete="CASCADE"), nullable=False, index=True)
    feature_name = Column(String(100), nullable=False)
    feature_value = Column(Float, nullable=True)
    shap_value = Column(Float, nullable=False)
    explanation_metadata = Column(JSON, nullable=True)

    prediction = relationship("RiskPrediction", back_populates="explanations")


class Intervention(Base):
    __tablename__ = "interventions"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    intervention_type = Column(String(100), nullable=False)
    assigned_reviewer = Column(String(100), nullable=False)
    created_date = Column(Date, default=datetime.date.today, nullable=False)
    planned_date = Column(Date, nullable=True)
    status = Column(String(50), default="PLANNED", nullable=False)  # PLANNED, IN_PROGRESS, COMPLETED, CANCELLED
    notes = Column(Text, nullable=True)

    employee = relationship("Employee", back_populates="interventions")
    outcomes = relationship("InterventionOutcome", back_populates="intervention", cascade="all, delete-orphan")


class InterventionOutcome(Base):
    __tablename__ = "intervention_outcomes"

    id = Column(Integer, primary_key=True, index=True)
    intervention_id = Column(Integer, ForeignKey("interventions.id", ondelete="CASCADE"), nullable=False, index=True)
    outcome_date = Column(Date, default=datetime.date.today, nullable=False)
    outcome_category = Column(String(100), nullable=False)  # Retained, Departed, Role Change, In Progress
    reviewer_notes = Column(Text, nullable=True)
    verification_status = Column(String(50), default="PENDING", nullable=False)

    intervention = relationship("Intervention", back_populates="outcomes")


class DataImportJob(Base):
    __tablename__ = "data_import_jobs"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    uploaded_by = Column(String(100), nullable=True)
    status = Column(String(50), default="PROCESSING", nullable=False)  # PENDING, PROCESSING, COMPLETED, FAILED
    total_rows = Column(Integer, default=0)
    successful_rows = Column(Integer, default=0)
    failed_rows = Column(Integer, default=0)
    failure_details = Column(JSON, nullable=True)
    import_summary = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action = Column(String(100), nullable=False, index=True)
    resource_type = Column(String(100), nullable=False)
    resource_id = Column(String(100), nullable=True)
    details = Column(JSON, nullable=True)
    ip_address = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    user = relationship("User", back_populates="audit_logs")
