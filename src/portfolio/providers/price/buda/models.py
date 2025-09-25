from pydantic import BaseModel


class _BudaMarketResponse(BaseModel):
    base_currency: str
    quote_currency: str
    id: str
    name: str | None = None
    minimum_order_amount: list | None = None
    disabled: bool | None = None
    illiquid: bool | None = None
    rpo_disabled: bool | None = None
    taker_fee: float | None = None
    maker_fee: float | None = None
    max_orders_per_minute: int | None = None
    maker_discount_percentage: str | None = None
    taker_discount_percentage: str | None = None
    taker_discount_tiers: dict | None = None
    maker_discount_tiers: dict | None = None


class BudaMarketsResponse(BaseModel):
    markets: list[_BudaMarketResponse]


class _BudaMarketTickerResponse(BaseModel):
    market_id: str
    last_price: list
    min_ask: list
    max_bid: list
    volume: list
    price_variation_24h: float
    price_variation_7d: float


class BudaMarketTickerResponse(BaseModel):
    ticker: _BudaMarketTickerResponse
