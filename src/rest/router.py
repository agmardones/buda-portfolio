from fastapi import APIRouter

from src.portfolio.providers.price.buda.provider import BudaPriceProvider
from src.portfolio.service import PortfolioService
from src.rest.schemas.request.portfolio import PortfolioValueRequest
from src.rest.schemas.responses.portfolio import PortfolioValueResponse


router = APIRouter()


@router.post("/portfolio/value")
def portfolio_value(request: PortfolioValueRequest) -> PortfolioValueResponse:
    service = PortfolioService(price_provider=BudaPriceProvider())
    service.validate_portfolio(
        portfolio=request.portfolio, target_currency=request.fiat_currency
    )
    return PortfolioValueResponse(value=1000)
