from fastapi import APIRouter

from src.rest.schemas.request.portfolio import PortfolioValueRequest
from src.rest.schemas.responses.portfolio import PortfolioValueResponse


router = APIRouter()


@router.post("/portfolio/value")
def portfolio_value(request: PortfolioValueRequest) -> PortfolioValueResponse:
    return PortfolioValueResponse(value=1000)
