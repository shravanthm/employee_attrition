# Repository Audit — AttritionPulse AI

**Date:** 2026-11-15  
**Audited by:** Phase 0 — Clone Verification & Project Setup  
**Repository:** https://github.com/code-dev-with-shruti/workforce-attrition-ai  
**Commit:** `4b969b0` — "add IBM HR dataset"  
**Branch:** `main` (single branch, 15 total commits)

---

## 1. Directory Structure (Actual)

```text
workforce-attrition-ai/
├── .gitignore
├── README.md
├── WA_Fn-UseC_-HR-Employee-Attrition.csv          # 1470 rows, 35 columns (IBM HR dataset)
│
├── attritioniq/
│   └── backend/
│       ├── main.py                                  # FastAPI app entry point
│       ├── database.py                              # SQLAlchemy engine + session
│       ├── models.py                                # Employee ORM model
│       ├── schemas.py                               # Pydantic schemas
│       ├── load_data.py                             # CSV → PostgreSQL loader
│       ├── train_model.py                           # XGBoost classifier training
│       ├── train_survival.py                        # Cox PH survival model training
│       ├── predict.py                               # XGBoost inference + preprocessing
│       ├── shap_explain.py                          # SHAP TreeExplainer wrapper
│       ├── survival_predict.py                      # Cox survival timeline
│       ├── test_survival.py                         # Manual survival test script (not pytest)
│       ├── requirements.txt                         # Pinned dependency list
│       ├── WA_Fn-UseC_-HR-Employee-Attrition.csv   # Duplicate of root CSV
│       ├── xgb_model.pkl                            # Pre-trained XGBoost model (~406 KB)
│       ├── cox_model.pkl                            # Pre-trained Cox PH model (~324 KB)
│       ├── encoder.pkl                              # Label encoders
│       ├── feature_columns.pkl                      # Feature column list
│       └── routes/
│           ├── employees.py                         # GET /employees, GET /employees/{id}
│           ├── predictions.py                       # Predict, explain, survival, batch predict
│           └── chat.py                              # Gemini-powered HR assistant
│
└── frontend/
    └── attrition/
        ├── package.json                             # React 19 + Vite 8 + TailwindCSS 4
        ├── package-lock.json                        # Lock file (~174 KB)
        ├── vite.config.js
        ├── tailwind.config.js
        ├── eslint.config.js
        ├── index.html
        ├── public/
        │   ├── favicon.svg
        │   └── icons.svg
        └── src/
            ├── main.jsx
            ├── App.jsx                              # React Router (BrowserRouter)
            ├── App.css                              # Legacy Vite starter CSS (commented out)
            ├── index.css                            # Tailwind import + commented CSS
            ├── api/
            │   └── client.js                        # Axios → http://localhost:8000
            ├── assets/
            │   ├── hero.png
            │   ├── react.svg
            │   └── vite.svg
            ├── components/
            │   ├── Layout.jsx                       # Shell with sidebar (lucide icons)
            │   └── Sidebar.jsx                      # Duplicate sidebar (emoji icons, unused)
            └── pages/
                ├── Dashboard.jsx                    # Charts with hardcoded demo data
                ├── Employees.jsx                    # Employee table (API-connected)
                ├── Predictions.jsx                  # Per-employee prediction panel
                ├── Chat.jsx                         # Gemini chat interface
                └── Upload.jsx                       # CSV upload UI (no backend endpoint)
```

---

## 2. Technology Inventory (Actual Versions)

### Runtime Environment

| Tool | Version (local) | Status |
|---|---|---|
| Python | 3.11.4 | ✅ Installed |
| Node.js | 24.11.1 | ✅ Installed |
| npm | 11.6.2 | ✅ Installed |
| Git | 2.51.0 | ✅ Installed |
| Docker | 29.3.1 | ⚠️ Installed but daemon NOT running |
| Docker Compose | 5.1.1 | ⚠️ Installed but no docker-compose.yml in repo |
| PostgreSQL (psql) | — | ❌ Not on PATH / not installed locally |

### Backend Dependencies (from `requirements.txt`)

| Package | Pinned Version | Local Installed | Notes |
|---|---|---|---|
| FastAPI | 0.136.3 | 0.110.0 | ⚠️ Mismatch — requirements ahead of local |
| SQLAlchemy | 2.0.50 | 2.0.43 | ⚠️ Mismatch |
| Pydantic | 2.13.4 | 2.9.2 | ⚠️ Mismatch |
| XGBoost | 3.2.0 | 3.2.0 | ✅ Match |
| SHAP | 0.51.0 | 0.51.0 | ✅ Match |
| scikit-learn | 1.9.0 | 1.7.2 | ⚠️ Mismatch |
| lifelines | 0.30.3 | ❌ Not installed | ❌ Missing |
| imbalanced-learn | — | ❌ Not installed | ❌ Missing (needed for SMOTE in training) |
| psycopg2-binary | 2.9.12 | ❌ Not verified | Required for PostgreSQL |
| Ollama | 0.6.2 | — | ⚠️ Listed in requirements.txt but code uses Gemini API |
| uvicorn | 0.48.0 | — | ASGI server |
| joblib | 1.5.3 | — | Model serialization |
| python-dotenv | 1.2.2 | — | .env loading |
| NumPy | 2.4.6 | — | Array operations |
| Pandas | 2.3.3 | — | Data manipulation |
| matplotlib | 3.10.9 | — | Listed but not used in API code |
| google-generativeai | — | — | ⚠️ NOT in requirements.txt but referenced in README |

### Frontend Dependencies (from `package.json`)

| Package | Version | Status |
|---|---|---|
| React | ^19.2.6 | ⚠️ Not installed (node_modules absent) |
| React DOM | ^19.2.6 | ⚠️ Not installed |
| Vite | ^8.0.12 | ⚠️ Not installed |
| @tailwindcss/vite | ^4.3.1 | ⚠️ Not installed |
| react-router-dom | ^7.17.0 | ⚠️ Not installed |
| axios | ^1.18.0 | ⚠️ Not installed |
| recharts | ^3.8.1 | ⚠️ Not installed |
| lucide-react | ^1.18.0 | ⚠️ Not installed |
| react-markdown | ^10.1.0 | ⚠️ Not installed |
| @vitejs/plugin-react | ^6.0.1 | ⚠️ Not installed |

> **All 18 frontend dependencies are UNMET.** `npm install` has not been run.

### Language & Configuration

| Aspect | Actual |
|---|---|
| Frontend language | **JavaScript (JSX)** — NOT TypeScript |
| Backend ASGI framework | FastAPI with raw uvicorn |
| ORM pattern | SQLAlchemy 2.x declarative_base (legacy import path) |
| Charting library | Recharts (not Plotly.js) |
| Tailwind version | v4 via `@tailwindcss/vite` plugin |
| CSS approach | Tailwind utility classes + commented Vite starter CSS |

---

## 3. Existing Features Assessment

### ✅ Implemented and Functional (if dependencies met)

| Feature | File(s) | Quality |
|---|---|---|
| XGBoost classifier | `train_model.py`, `predict.py`, `xgb_model.pkl` | Working — SMOTE, threshold 0.25, risk tiers |
| Cox PH survival model | `train_survival.py`, `survival_predict.py`, `cox_model.pkl` | Working — balanced oversampling, penalizer=0.1 |
| SHAP explainability | `shap_explain.py` | Working — TreeExplainer, top 3 factors |
| Employee ORM model | `models.py` | Working — maps IBM HR dataset columns |
| Pydantic schemas | `schemas.py` | Working — EmployeeBase + EmployeeResponse |
| REST API (employees) | `routes/employees.py` | Working — list all, get by ID |
| REST API (predictions) | `routes/predictions.py` | Working — predict single, batch, explain, survival |
| REST API (chat) | `routes/chat.py` | Working — Gemini 2.5-flash integration |
| CSV data loader | `load_data.py` | Working — drops useless cols, seeds DB |
| Frontend Dashboard | `pages/Dashboard.jsx` | **Partial** — hardcoded demo data, not API-connected for charts |
| Frontend Employees | `pages/Employees.jsx` | Working — API-connected table with search |
| Frontend Predictions | `pages/Predictions.jsx` | Working — triggers predict + SHAP + survival |
| Frontend Chat | `pages/Chat.jsx` | Working — Gemini chat with quick prompts |
| Frontend Upload | `pages/Upload.jsx` | **Broken** — calls `/employees/upload-csv` which does not exist |
| Dark mode toggle | `Layout.jsx` | Working — CSS class-based dark mode |

### ❌ Not Implemented

| Missing Component | Impact |
|---|---|
| Upload CSV API endpoint | Frontend Upload page is non-functional |
| Alembic migrations | No schema versioning; `load_data.py` drops and recreates all tables |
| Authentication / authorization | No auth — entire API is open |
| Docker Compose | No containerization config |
| .env.example | Listed in .gitignore but not committed |
| Any tests (pytest, vitest) | `test_survival.py` is a manual script, not a test framework |
| CI/CD pipeline | No GitHub Actions or similar |
| API rate limiting | Open CORS (`*`) + no throttling |
| Input validation on routes | Minimal — no CSV validation, no request body validation on chat |
| Error handling | Basic — predict_all silently catches all exceptions |
| Logging | Print statements only |

---

## 4. Data Assessment

### IBM HR Employee Attrition Dataset

| Property | Value |
|---|---|
| File | `WA_Fn-UseC_-HR-Employee-Attrition.csv` |
| Rows | 1,470 employees |
| Columns | 35 |
| Duplicated | Yes — same CSV at root and inside `attritioniq/backend/` |
| Source | IBM Watson Analytics sample data |
| License | Public domain / CC0 — freely usable |
| Real employee data | **No** — fictional/synthetic IBM sample data |

### Dataset Columns (35)

```
Age, Attrition, BusinessTravel, DailyRate, Department, DistanceFromHome,
Education, EducationField, EmployeeCount, EmployeeNumber,
EnvironmentSatisfaction, Gender, HourlyRate, JobInvolvement, JobLevel,
JobRole, JobSatisfaction, MaritalStatus, MonthlyIncome, MonthlyRate,
NumCompaniesWorked, Over18, OverTime, PercentSalaryHike,
PerformanceRating, RelationshipSatisfaction, StandardHours,
StockOptionLevel, TotalWorkingYears, TrainingTimesLastYear,
WorkLifeBalance, YearsAtCompany, YearsInCurrentRole,
YearsSinceLastPromotion, YearsWithCurrManager
```

### Columns Dropped by Training Scripts

- `EmployeeCount` (constant = 1)
- `StandardHours` (constant = 80)
- `Over18` (constant = "Y")
- `EmployeeNumber` (identifier, not a feature)

---

## 5. Code Quality Issues

### Critical

1. **Hardcoded file paths** — `train_model.py` line 10 and `train_survival.py` line 48 reference `C:/Users/KIIT01/Desktop/Revised_Full_Stack_Project/...` — will crash on any other machine.
2. **Model loading uses bare filenames** — `predict.py` loads `xgb_model.pkl` relative to CWD, not to the module directory. Works only when `uvicorn` is started from `attritioniq/backend/`.
3. **Import paths assume CWD** — `main.py` imports `from database import Base` using relative imports that only work with specific `uvicorn` invocation (`attritioniq.backend.main:app` does NOT work — it errors because Python can't resolve `database` without `attritioniq.backend.database`).
4. **Database drops all data on every load** — `load_data.py` calls `Base.metadata.drop_all()` before insert — destructive.
5. **No `__init__.py` files** — The `attritioniq/` and `attritioniq/backend/` directories lack `__init__.py`, making package imports unreliable.
6. **Duplicate employee_dict construction** — The same 27-field dict is manually constructed in 5 places across `routes/predictions.py` — a prime refactoring target.

### Security

1. **CORS is fully open** — `allow_origins=["*"]` in production would be a vulnerability.
2. **No authentication** — Any network client can read all employee data and trigger predictions.
3. **Gemini API key in .env** — Correctly not committed, but no `.env.example` is provided.
4. **API key passed as URL query parameter** in `chat.py` — visible in logs and browser history.

### Warnings

1. **Sidebar component duplication** — `Layout.jsx` (lucide icons, actually used) and `Sidebar.jsx` (emoji icons, imported nowhere) — `Sidebar.jsx` is dead code.
2. **App.jsx has ~120 lines of commented-out Vite starter code.**
3. **index.css has ~100 lines of commented-out Vite starter CSS.**
4. **App.css is entirely Vite starter CSS** — not used by the current app.
5. **Dashboard uses hardcoded data** — `deptData`, `pieData`, `survivalData`, and "Top flight risks" are all static, not from the API.
6. **`ollama` package in requirements.txt** — The code migrated to Gemini but Ollama is still listed as a dependency.
7. **`google-generativeai` NOT in requirements.txt** — The README mentions it but `chat.py` actually uses raw `urllib` HTTP calls, so it's not actually needed. However, the README install instructions list it.
8. **`matplotlib` in requirements.txt** — Not imported or used anywhere in the API code.
9. **`use_label_encoder=False` in train_model.py** — Deprecated XGBoost parameter.

---

## 6. Run Status

### Backend

| Step | Result |
|---|---|
| `DATABASE_URL` set? | ❌ No `.env` file, no PostgreSQL running |
| PostgreSQL reachable? | ❌ `psql` not on PATH, no Docker PostgreSQL container |
| `python main.py` | ❌ Fails — `RuntimeError: DATABASE_URL environment variable is not set` |
| Model .pkl files present? | ✅ `xgb_model.pkl`, `cox_model.pkl`, `encoder.pkl`, `feature_columns.pkl` |
| Re-training possible? | ❌ Hardcoded paths in train scripts + missing `lifelines`/`imbalanced-learn` |

### Frontend

| Step | Result |
|---|---|
| `node_modules/` present? | ❌ Not installed |
| `npm install` possible? | ✅ `package-lock.json` present, should resolve |
| `npm run dev` | ❌ Cannot run until `npm install` completes |

### Overall

**Neither frontend nor backend can currently run.** The primary blockers are:
1. No PostgreSQL instance available.
2. Missing Python dependencies (`lifelines`, `imbalanced-learn`).
3. Frontend `node_modules` not installed.
4. No `.env` file with `DATABASE_URL` and `GEMINI_API_KEY`.
