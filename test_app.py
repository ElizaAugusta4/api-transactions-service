import pytest
from fastapi.testclient import TestClient
from transactions_service.app import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Transactions Service" in response.json()["message"]

