from collections.abc import AsyncGenerator
from typing import Protocol, TypeVar

import pydantic as py

T = TypeVar("T", bound=py.BaseModel)


class ExchangeConnectorProtocol(Protocol):
    def __call__(self, pair: str) -> AsyncGenerator[T]: ...
