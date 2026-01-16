"""
Tests for the FastAPI endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints."""

    def test_root_endpoint(self):
        """Root endpoint returns health status."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data

    def test_health_endpoint(self):
        """Health endpoint returns health status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestEvaluateEndpoint:
    """Test the main evaluation endpoint."""

    def test_evaluate_vat_registered(self):
        """VAT registered taxpayer is not eligible."""
        response = client.post(
            "/api/v1/simplified-tax/evaluate",
            json={"is_vat_registered": True},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["eligible"] is False
        assert data["reason_code"] == "VAT_REGISTERED"

    def test_evaluate_eligible_general(self):
        """Non-VAT registered with low turnover is eligible."""
        response = client.post(
            "/api/v1/simplified-tax/evaluate",
            json={
                "is_vat_registered": False,
                "turnover": {
                    "gross_turnover_12m": 150000,
                },
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["eligible"] is True
        assert data["route"] == "general"
        assert data["tax_amount"] == "3000.00"  # 150000 × 2%

    def test_evaluate_with_debug(self):
        """Debug mode includes trace."""
        response = client.post(
            "/api/v1/simplified-tax/evaluate?debug=1",
            json={
                "is_vat_registered": False,
                "turnover": {
                    "gross_turnover_12m": 100000,
                },
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["debug_trace"] is not None
        assert len(data["debug_trace"]) > 0

    def test_evaluate_property_transfer_exempt(self):
        """Property transfer with 3-year registration is exempt."""
        response = client.post(
            "/api/v1/simplified-tax/evaluate",
            json={
                "is_vat_registered": False,
                "route_auto_property": True,
                "property_transfer": {
                    "property_type": "residential",
                    "area_m2": 100,
                    "location_zone": "baku_center",
                    "is_registered_3yr": True,
                },
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["eligible"] is True
        assert data["tax_amount"] == "0"

    def test_evaluate_licensed_activity_not_eligible(self):
        """Licensed activity without carve-out is not eligible."""
        response = client.post(
            "/api/v1/simplified-tax/evaluate",
            json={
                "is_vat_registered": False,
                "licensed_activity_codes": ["private_medical"],
                "turnover": {
                    "gross_turnover_12m": 100000,
                },
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["eligible"] is False
        assert data["reason_code"] == "LICENSED_ACTIVITY"

    def test_evaluate_licensed_activity_with_carveout_eligible(self):
        """Licensed activity with compulsory insurance carve-out is eligible."""
        response = client.post(
            "/api/v1/simplified-tax/evaluate",
            json={
                "is_vat_registered": False,
                "licensed_activity_codes": ["private_medical"],
                "has_compulsory_insurance_carveout": True,
                "turnover": {
                    "gross_turnover_12m": 100000,
                },
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["eligible"] is True


class TestQuestionsEndpoint:
    """Test the questions endpoint."""

    def test_get_questions(self):
        """Get all interview questions."""
        response = client.get("/api/v1/simplified-tax/questions")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

        # Check first question structure
        first_q = data[0]
        assert "id" in first_q
        assert "type" in first_q
        assert "question" in first_q
        assert "question_az" in first_q

    def test_get_single_question(self):
        """Get a specific question by ID."""
        response = client.get("/api/v1/simplified-tax/questions/vat_registration")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "vat_registration"
        assert data["type"] == "boolean"

    def test_get_nonexistent_question(self):
        """Get a nonexistent question returns 404."""
        response = client.get("/api/v1/simplified-tax/questions/nonexistent")
        assert response.status_code == 404


class TestLicensedActivitiesEndpoint:
    """Test the licensed activities endpoint (PATCH 3)."""

    def test_get_all_licensed_activities(self):
        """Get all licensed activities."""
        response = client.get("/api/v1/simplified-tax/licensed-activities")
        assert response.status_code == 200
        data = response.json()
        assert "activities" in data
        assert "categories" in data
        assert len(data["activities"]) > 0

    def test_search_licensed_activities(self):
        """Search licensed activities by name."""
        response = client.get(
            "/api/v1/simplified-tax/licensed-activities?search=medical"
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["activities"]) > 0
        assert any("medical" in a["name_en"].lower() for a in data["activities"])

    def test_filter_licensed_activities_by_category(self):
        """Filter licensed activities by category."""
        response = client.get(
            "/api/v1/simplified-tax/licensed-activities?category=healthcare"
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["activities"]) > 0
        assert all(a["category"] == "healthcare" for a in data["activities"])


class TestQuestionCount:
    """Test that question count is within limits."""

    def test_max_15_top_level_questions(self):
        """Verify ≤15 top-level questions as per requirements."""
        response = client.get("/api/v1/simplified-tax/questions")
        assert response.status_code == 200
        data = response.json()

        # Count only top-level questions (not subquestions)
        top_level_count = len(data)
        assert top_level_count <= 15, f"Expected ≤15 questions, got {top_level_count}"
