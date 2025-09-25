from decimal import Decimal

from fastapi import HTTPException
from src.portfolio.providers.price.interface import PriceProviderInterface
from src.shared.types import PortfolioType


class PortfolioService:
    def __init__(self, price_provider: PriceProviderInterface):
        self.price_provider = price_provider

    def _build_market_id(self, asset: str, target_currency: str) -> str:
        return f"{asset}-{target_currency}".lower()

    def validate_portfolio_assets(
        self, portfolio: PortfolioType, target_currency: str
    ) -> None:
        valid_markets = self.price_provider.get_valid_markets()
        for asset, _ in portfolio.items():
            market = self._build_market_id(asset, target_currency)
            if market not in valid_markets:
                raise HTTPException(status_code=400, detail=f"Invalid asset: {asset}")
        return None

    def get_portfolio_value(
        self, portfolio: PortfolioType, target_currency: str
    ) -> Decimal:
        value = Decimal(0)
        for asset, amount in portfolio.items():
            market = self._build_market_id(asset, target_currency)
            price = self.price_provider.get_market_price(market)
            value += price * amount
        return value
