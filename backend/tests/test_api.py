"""Integration and API endpoint tests for AttritionPulse AI."""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_api_health_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["service"] == "AttritionPulse AI API"


@pytest.mark.asyncio
async def test_dashboard_metrics_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/api/v1/metrics/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "total_employees" in data
    assert "high_risk_count" in data
    assert "department_distribution" in data


@pytest.mark.asyncio
async def test_predict_endpoint_with_shap():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post("/api/v1/predictions/1")
    assert response.status_code == 200
    data = response.json()
    assert "risk_probability" in data
    assert "risk_category" in data
    assert len(data["top_explanations"]) > 0


@pytest.mark.asyncio
async def test_survival_timeline_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/api/v1/survival/1")
    assert response.status_code == 200
    data = response.json()
    assert data["employee_id"] == 1
    assert "survival_timeline" in data
    assert len(data["survival_timeline"]) == 5
    assert data["survival_timeline"][0]["horizon_days"] == 30
