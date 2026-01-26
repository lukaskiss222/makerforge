from pydantic import BaseModel, Field


class CoinmateSettings(BaseModel):
    websocket: str = Field("wss://coinmate.io/api/websocket/channel", description="Websocket url for coinmate.")
    pair: str = Field(
        ...,
        description="Coinmate pair like BTC_EUR.",
    )
