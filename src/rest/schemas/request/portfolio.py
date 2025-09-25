from pydantic import BaseModel

from src.shared.types import PortfolioType


class PortfolioValueRequest(BaseModel):
    portfolio: PortfolioType
    fiat_currency: str
