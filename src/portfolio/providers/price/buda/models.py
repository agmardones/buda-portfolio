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
