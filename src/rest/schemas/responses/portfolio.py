from pydantic import BaseModel


class PortfolioValueResponse(BaseModel):
    value: float
