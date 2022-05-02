"Script which contains several utils for Haldis"

import re
from typing import Iterable, Optional


def euro_string(value: int, unit="€ ") -> str:
    """
    Convert cents to string formatted euro
    """
    euro, cents = divmod(value, 100)
    if cents:
        return f"{unit}{euro}.{cents:02}"
    return f"{unit}{euro}"


def parse_euro_string(value: str) -> Optional[int]:
    m = re.fullmatch("(?:€ ?)?([0-9]+)(?:[.,]([0-9]+))?", value)
    if not m:
        return None
    cents_02 = "{:0<2.2}".format(m.group(2)) if m.group(2) else "00"
    return int(m.group(1)) * 100 + int(cents_02)


def price_range_string(price_range, include_upper=False):
    "Convert a price range to a string formatted euro"
    if price_range[0] == price_range[1]:
        return euro_string(price_range[0])
    return ("{}—{}" if include_upper else "from {}").format(
        *map(euro_string, price_range)
    )


def first(iterable: Iterable, default=None):
    """
    Return first element of iterable
    """
    try:
        return next(iter(iterable))
    except StopIteration:
        return default


def ignore_none(iterable: Iterable):
    "Filter to ignore None objects"
    return filter(lambda x: x is not None, iterable)
