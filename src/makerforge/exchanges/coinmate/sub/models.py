from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, RootModel
from pydantic.types import PositiveFloat, PositiveInt


class LimitModel(BaseModel):
    price: PositiveFloat
    amount: PositiveFloat
    # Drop these
    # amountSum: PositiveFloat
    # cumulativePrice: PositiveFloat
    # wholePartDiffers: bool


class OrderBookModel(BaseModel):
    bids: list[LimitModel]
    asks: list[LimitModel]


class TradeType(Enum):
    buy = "BUY"
    sell = "SELL"


class TradeModel(BaseModel):
    date: PositiveInt
    price: PositiveFloat
    amount: PositiveFloat
    buyOrderId: PositiveInt
    sellOrderId: PositiveInt
    total: PositiveFloat
    type: TradeType


class DataEvent(BaseModel):
    event: Literal["data"]
    channel: str


class DataTradeEvent(DataEvent):
    payload: list[TradeModel]


class DataOrderBookEvent(DataEvent):
    payload: OrderBookModel


class DataPingEvent(BaseModel):
    event: Literal["ping"]


class DataPongEvent(BaseModel):
    event: Literal["pong"]


class DataErrorEvent(BaseModel):
    event: Literal["error"]
    message: str


class CoinmateTradeResponse(RootModel):
    root: DataPingEvent | DataTradeEvent | DataPongEvent | DataErrorEvent = Field(discriminator="event")


class CoinmateOrderBookResponse(RootModel):
    root: DataPingEvent | DataOrderBookEvent | DataPongEvent | DataErrorEvent = Field(discriminator="event")
