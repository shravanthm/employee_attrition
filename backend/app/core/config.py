"""Application Configuration for AttritionPulse AI.
Supports PostgreSQL (via psycopg) with SQLite local fallback if PostgreSQL is unavailable.
"""

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENVIRONMENT: str = Field(default="development", description="Environment: development, test, production")
    LOG_LEVEL: str = Field(default="INFO", description="Log level")

    # PostgreSQL configuration
    POSTGRES_USER: str = "attrition_user"
    POSTGRES_PASSWORD: str = "attrition_secret_pass"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "attritionpulse"

    # Database URLs
    DATABASE_URL: str = Field(
        default="postgresql+psycopg://attrition_user:attrition_secret_pass@localhost:5432/attritionpulse",
        description="Primary database connection string"
    )
    TEST_DATABASE_URL: str = Field(
        default="postgresql+psycopg://attrition_user:attrition_secret_pass@localhost:5433/attritionpulse_test",
        description="Test database connection string"
    )
    
    # SQLite Fallback Path (enables zero-friction local execution if Docker daemon is not active)
    SQLITE_FALLBACK_URL: str = "sqlite:///./data/attritionpulse.db"
    SQLITE_TEST_FALLBACK_URL: str = "sqlite:///./data/attritionpulse_test.db"

    # Security
    SECRET_KEY: str = Field(
        default="insecure-dev-key-must-be-changed-in-production-at-least-32-chars",
        description="HMAC secret key"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]

    # External AI
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",") if i.strip()]
        return v


settings = Settings()
