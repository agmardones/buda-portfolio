from decimal import Decimal
from pydantic import BaseModel


class PortfolioValueResponse(BaseModel):
    value: Decimal
