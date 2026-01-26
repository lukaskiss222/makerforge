import pydantic as py
import redis.asyncio as redis
from redis.typing import EncodableT, FieldT

from infrastructure.ioc import get_container
from makerforge.settings import Settings


async def stream_key(exchange: str, channel: str, pair: str, prefix: str | None = None) -> str:
    if prefix is None:
        container = get_container()
        settings = await container.get(Settings)
        prefix = settings.redis_stream_prefix
    return f"{prefix}:{exchange}:{channel}:{pair}"


async def add_stream_entry(
    redis_client: redis.Redis,
    key: str,
    entry: py.BaseModel,
    id: str = "*",
) -> None:
    entry_json: dict[FieldT, EncodableT] = {
        "data": entry.model_dump_json(),
        "type": entry.__class__.__name__,
    }
    await redis_client.xadd(
        key,
        entry_json,
        id=id,
        approximate=True,
        maxlen=2 * 3600 * 48,
    )
