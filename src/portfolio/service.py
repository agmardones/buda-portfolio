from decimal import Decimal

from fastapi import HTTPException
from src.portfolio.providers.price.interface import PriceProviderInterface
from src.shared.types import PortfolioType


class PortfolioService:
    def __init__(self, price_provider: PriceProviderInterface):
        self.price_provider = price_provider

    def validate_portfolio(
        self, portfolio: PortfolioType, target_currency: str
    ) -> None:
        valid_markets = self.price_provider.get_valid_markets()
        for asset, _ in portfolio.items():
            market = f"{asset}-{target_currency}".lower()
            if market not in valid_markets:
                raise HTTPException(status_code=400, detail=f"Invalid asset: {asset}")
        return None
