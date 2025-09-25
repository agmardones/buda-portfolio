from fastapi.testclient import TestClient
from src.main import app
from pytest_mock import MockerFixture
from src.portfolio.providers.price.buda.provider import BudaPriceProvider


client = TestClient(app)


def test_health_endpoint():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "healthy"}


def test_portfolio_value_endpoint_invalid_assert(mocker: MockerFixture):
    mocker.patch.object(
        BudaPriceProvider,
        "get_valid_markets",
        return_value=["btc-clp", "eth-clp", "usdt-clp"],
    )
    data = {
        "portfolio": {"BTC": 1, "ETH": 2, "USDT": 3, "INVALID": 4},
        "fiat_currency": "CLP",
    }
    resp = client.post("/portfolio/value", json=data)
    assert resp.status_code == 400


def test_portfolio_value_endpoint_valid_assert(mocker: MockerFixture):
    mocker.patch.object(
        BudaPriceProvider,
        "get_valid_markets",
        return_value=["btc-clp", "eth-clp", "usdt-clp"],
    )
    mocker.patch.object(BudaPriceProvider, "get_market_price", return_value=10)
    data = {"portfolio": {"BTC": 1, "ETH": 2, "USDT": 3}, "fiat_currency": "CLP"}
    resp = client.post("/portfolio/value", json=data)
    assert resp.status_code == 200
    assert resp.json() == {"value": "60"}


def test_portfolio_value_endpoint_different_prices(mocker: MockerFixture):
    mocker.patch.object(
        BudaPriceProvider,
        "get_valid_markets",
        return_value=["btc-clp", "eth-clp", "usdt-clp"],
    )
    mocker.patch.object(
        BudaPriceProvider,
        "get_market_price",
        side_effect=[50000, 3000, 1],
    )
    data = {"portfolio": {"BTC": 1, "ETH": 2, "USDT": 3}, "fiat_currency": "CLP"}
    resp = client.post("/portfolio/value", json=data)
    assert resp.status_code == 200
    # Expected calculation: (1 * 50000) + (2 * 3000) + (3 * 1) = 50000 + 6000 + 3 = 56003
    assert resp.json() == {"value": "56003"}


def test_portfolio_value_endpoint_invalid_fiat_currency(mocker: MockerFixture):
    mocker.patch.object(
        BudaPriceProvider,
        "get_valid_markets",
        return_value=["btc-clp", "eth-clp", "usdt-clp"],
    )
    data = {"portfolio": {"BTC": 1, "ETH": 2, "USDT": 3}, "fiat_currency": "INVALID"}
    resp = client.post("/portfolio/value", json=data)
    assert resp.status_code == 400
