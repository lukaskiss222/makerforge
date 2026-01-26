import logging
from collections.abc import AsyncGenerator

import pydantic as py
from websockets.asyncio.client import connect

from makerforge.errors.pydantic_utils import compact_errors

from .models import CoinmateOrderBookResponse, CoinmateTradeResponse

logger = logging.getLogger(__name__)


async def connect_orderbook(pair: str) -> AsyncGenerator[CoinmateOrderBookResponse]:
    async with connect(f"wss://coinmate.io/api/websocket/channel/order-book/{pair}") as ws:
        logger.info("Connected to Coinmate order book websocket.")
        while True:
            temp_message = await ws.recv()
            try:
                message = CoinmateOrderBookResponse.model_validate_json(temp_message, strict=True)
                yield message
            except py.ValidationError as e:
                compact, total = compact_errors(e)
                logger.error(
                    "Failed to parse order book message",
                    extra={
                        "pair": pair,
                        "msg_bytes": len(temp_message),
                        "error_count": total,
                        "errors": compact,
                    },
                )


async def connect_trades(pair: str) -> AsyncGenerator[CoinmateTradeResponse]:
    async with connect(f"wss://coinmate.io/api/websocket/channel/trades/{pair}") as ws:
        logger.info("Connected to Coinmate trades websocket.")
        while True:
            temp_message = await ws.recv()
            try:
                message = CoinmateTradeResponse.model_validate_json(temp_message, strict=True)
                yield message
            except py.ValidationError as e:
                compact, total = compact_errors(e)
                logger.error(
                    "Failed to parse trades message",
                    extra={
                        "pair": pair,
                        "msg_bytes": len(temp_message),
                        "error_count": total,
                        "errors": compact,
                    },
                )
