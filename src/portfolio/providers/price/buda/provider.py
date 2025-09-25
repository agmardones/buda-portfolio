from decimal import Decimal
from src.portfolio.providers.price.buda.client import BudaClient
from src.shared.types import PortfolioType
from src.portfolio.providers.price.interface import PriceProviderInterface


class BudaPriceProvider(PriceProviderInterface):
    def __init__(self):
        self.client = BudaClient()

    def get_valid_markets(self) -> list[str]:
        return [market.id.lower() for market in self.client.get_markets().markets]

    def get_portfolio_value(
        self, portfolio: PortfolioType, target_currency: str
    ) -> Decimal:
        return Decimal(0)
