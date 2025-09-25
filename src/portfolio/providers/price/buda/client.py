from src.portfolio.providers.price.buda.models import BudaMarketsResponse
from src.shared.http_client import create_client


class BudaClient:
    def __init__(self):
        self.http_client = create_client(base_url="https://www.buda.com/api/v2")

    def get_markets(self) -> BudaMarketsResponse:
        response = self.http_client.get("/markets")
        return BudaMarketsResponse.model_validate(response.json())
