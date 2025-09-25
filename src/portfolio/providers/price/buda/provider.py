from decimal import Decimal
from src.portfolio.providers.price.buda.client import BudaClient
from src.portfolio.providers.price.interface import PriceProviderInterface


class BudaPriceProvider(PriceProviderInterface):
    def __init__(self):
        self.client = BudaClient()

    def get_valid_markets(self) -> list[str]:
        return [market.id.lower() for market in self.client.get_markets().markets]

    def get_market_price(self, market: str) -> Decimal:
        return Decimal(self.client.get_market_price(market).ticker.last_price[0])
