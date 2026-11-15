"""Main FastAPI application entrypoint for AttritionPulse AI."""

from app.api.v1.endpoints import router as api_v1_router, upload_employees_csv, ask_chat
from app.core.config import settings
from app.db.session import Base, engine, SessionLocal
from app.db.auto_seed import auto_seed_if_empty
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Auto create tables on boot if not existing (e.g. SQLite fallback)
Base.metadata.create_all(bind=engine)

# Auto seed on boot if empty
try:
    _init_db = SessionLocal()
    auto_seed_if_empty(_init_db)
    _init_db.close()
except Exception:
    pass

app = FastAPI(
    title="AttritionPulse AI API",
    description="Longitudinal Employee Attrition Early-Warning & Explainable Risk Intelligence System",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Explicit CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

app.include_router(api_v1_router)

# Aliases for direct / legacy root paths
app.post("/employees/upload-csv", tags=["Data Ingestion"])(upload_employees_csv)
app.post("/chat/ask/{employee_id}", tags=["Chat"])(ask_chat)

@app.get("/", tags=["Health"])
@app.get("/api", tags=["Health"])
@app.get("/api/v1", tags=["Health"])
def health_check():
    return {
        "status": "online",
        "service": "AttritionPulse AI API",
        "environment": settings.ENVIRONMENT,
        "version": "2.0.0"
    }
