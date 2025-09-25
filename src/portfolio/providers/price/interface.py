from decimal import Decimal
from src.shared.types import PortfolioType


class PriceProviderInterface:
    def get_valid_markets(self) -> list[str]: ...

    def get_portfolio_value(
        self, portfolio: PortfolioType, target_currency: str
    ) -> Decimal: ...
