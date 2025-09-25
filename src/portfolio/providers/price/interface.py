from decimal import Decimal


class PriceProviderInterface:
    def get_valid_markets(self) -> list[str]: ...

    def get_market_price(self, market: str) -> Decimal: ...
