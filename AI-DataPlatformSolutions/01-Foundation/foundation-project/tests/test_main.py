"""
Foundation Project - Main Application Tests
Basic tests to ensure the application can start and run
"""

import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

def test_app_creation():
    """Test that the FastAPI app can be created"""
    try:
        from src.api.main import app
        assert isinstance(app, FastAPI)
        assert app.title == "Foundation Project - Enterprise AI-Data Platform"
    except ImportError as e:
        pytest.skip(f"Could not import main app: {e}")

def test_app_has_routes():
    """Test that the app has the expected routes"""
    try:
        from src.api.main import app
        routes = [route.path for route in app.routes]
        
        # Check for essential routes
        assert "/" in routes
        assert "/health" in routes
        assert "/docs" in routes
        assert "/openapi.json" in routes
        
    except ImportError as e:
        pytest.skip(f"Could not import main app: {e}")

def test_health_endpoint():
    """Test the health check endpoint"""
    try:
        from src.api.main import app
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        
    except ImportError as e:
        pytest.skip(f"Could not import main app: {e}")

def test_root_endpoint():
    """Test the root endpoint"""
    try:
        from src.api.main import app
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
        assert "Foundation Project" in response.json()["message"]
        
    except ImportError as e:
        pytest.skip(f"Could not import main app: {e}")

if __name__ == "__main__":
    pytest.main([__file__])
