from collections.abc import Callable

type ExportFn = Callable[[str], None]

# exporters: dict[str, ExportFn] = {
#    "coinmate": ...,
#    "binance": ...,
# }
