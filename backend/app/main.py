"""Main FastAPI application entrypoint for AttritionPulse AI."""

from app.api.v1.endpoints import router as api_v1_router, upload_employees_csv
from app.core.config import settings
from app.db.session import Base, engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Auto create tables on boot if not existing (e.g. SQLite fallback)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AttritionPulse AI API",
    description="Longitudinal Employee Attrition Early-Warning & Explainable Risk Intelligence System",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Explicit CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(api_v1_router)

# Support legacy / direct upload path
app.post("/employees/upload-csv", tags=["Data Ingestion"])(upload_employees_csv)

@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "online",
        "service": "AttritionPulse AI API",
        "environment": settings.ENVIRONMENT,
        "version": "2.0.0"
    }
