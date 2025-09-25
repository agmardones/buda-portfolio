from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_health_endpoint():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "healthy"}


def test_portfolio_value_endpoint():
    data = {"portfolio": {"BTC": 1, "ETH": 2, "USDT": 3}, "fiat_currency": "CLP"}
    resp = client.post("/portfolio/value", json=data)
    assert resp.status_code == 200
    assert resp.json() == {"value": 1000}
