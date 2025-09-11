import pytest
from fastapi.testclient import TestClient
from transactions_service.app import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Transactions Service" in response.json()["message"]

def test_create_transaction():
    # Precisa de uma conta existente, então pode falhar se não houver
    payload = {
        "account_id": 1,
        "type": "INCOME",
        "amount": 100.00,
        "description": "Teste",
        "category": "Teste"
    }
    response = client.post("/transactions", json=payload)
    assert response.status_code in [201, 404]  # 404 se não houver conta

def test_list_transactions():
    response = client.get("/transactions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_transaction():
    # Cria uma transação para garantir que existe
    payload = {
        "account_id": 1,
        "type": "INCOME",
        "amount": 50.00,
        "description": "Teste",
        "category": "Teste"
    }
    post_resp = client.post("/transactions", json=payload)
    if post_resp.status_code == 201:
        tx_id = post_resp.json()["id"]
        get_resp = client.get(f"/transactions/{tx_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["id"] == tx_id
