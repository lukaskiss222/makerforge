import pydantic as py


def compact_errors(e: py.ValidationError, limit: int = 5) -> tuple[list[dict], int]:
    errs = e.errors(include_url=False, include_input=False)
    compact = []
    for err in errs[:limit]:
        compact.append(
            {
                "loc": err.get("loc"),
                "msg": err.get("msg"),
                "type": err.get("type"),
            }
        )
    return compact, len(errs)
