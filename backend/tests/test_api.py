import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ─── TEST 1 — Home API ──────────────────
def test_home_api():
    print("\n🔍 Home API test...")
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    print("✅ Home API working!")

# ─── TEST 2 — Health API ────────────────
def test_health_api():
    print("\n🔍 Health API test...")
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    print("✅ Health API working!")

# ─── TEST 3 — Wrong URL ─────────────────
def test_wrong_url():
    print("\n🔍 Wrong URL test...")
    response = client.get("/wrong-url")
    assert response.status_code == 404
    print("✅ 404 correctly returned!")