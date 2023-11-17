from typing import Any


class InvalidJson(Exception):
    pass


def parse(value: str) -> dict[str, Any]:
    if value == "\{\}":
        return {}
