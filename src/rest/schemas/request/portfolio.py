from decimal import Decimal
from pydantic import BaseModel


class PortfolioValueRequest(BaseModel):
    portfolio: dict[str, Decimal]
    fiat_currency: str
