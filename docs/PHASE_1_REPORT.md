# Phase 1 Report — Development Environment & Database Foundation

**Project:** AttritionPulse AI  
**Date:** 2026-11-15  
**Status:** Completed & Verified ✅  

---

## 1. Environment & Dependencies

- **Python Runtime:** Python 3.11.4 verified compatible.
- **Dependencies Installed & Pinned:**
  - `SQLAlchemy==2.0.43`
  - `alembic==1.20.1`
  - `psycopg==3.3.9` & `psycopg-binary==3.3.9`
  - `argon2-cffi==25.1.0`
  - `pydantic==2.9.2` & `pydantic-settings==2.11.0`
  - `lifelines==0.30.3`
  - `imbalanced-learn==0.14.2`
  - `statsmodels==0.15.0`
  - `pytest==9.1.1`
- **Docker Compose:** Prepared `docker-compose.yml` with PostgreSQL 16 Alpine + health checks + test DB + named persistent volumes.
- **Resilient DB Session:** Built `app.db.session` with automatic graceful fallback to local SQLite (`data/attritionpulse.db`) if Docker daemon is not active on Windows 11 host.

---

## 2. Implemented Database Schema & Migrations

All 12 required tables were implemented in `backend/app/models/entities.py`:
1. `roles` (RBAC)
2. `users` (Argon2 authentication)
3. `employees` (Demographics and tenure)
4. `employee_monthly_snapshots` (12-factor longitudinal telemetry)
5. `attrition_events` (Survival events with censoring indicators)
6. `model_registry` (Model lifecycle and metrics)
7. `risk_predictions` (90-day horizon probabilities and risk tiers)
8. `prediction_explanations` (SHAP feature contributions)
9. `interventions` (Retention actions)
10. `intervention_outcomes` (Empirical outcome validation)
11. `data_import_jobs` (CSV upload provenance and error tracking)
12. `audit_logs` (Sensitive action auditing)

### Alembic Migration
Generated and executed revision `d5a423cbd719_create_initial_phase1_tables.py`:
```text
INFO [alembic.runtime.migration] Running upgrade -> d5a423cbd719, create_initial_phase1_tables
```

---

## 3. Test Results

Executed test suite using pytest (`pytest tests/ -v`):
```text
tests/test_database.py::test_environment_and_config PASSED               [ 16%]
tests/test_database.py::test_argon2_password_hashing PASSED              [ 33%]
tests/test_database.py::test_role_and_user_creation PASSED               [ 50%]
tests/test_database.py::test_employee_and_snapshot_creation PASSED       [ 66%]
tests/test_database.py::test_snapshot_unique_constraint PASSED           [ 83%]
tests/test_database.py::test_attrition_event_and_prediction PASSED       [100%]

============================== 6 passed in 7.18s ==============================
```
