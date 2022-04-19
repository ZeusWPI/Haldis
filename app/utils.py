"Script which contains several utils for Haldis"

from typing import Iterable


def euro_string(value: int) -> str:
    """
    Convert cents to string formatted euro
    """
    euro, cents = divmod(value, 100)
    if cents:
        return f"€ {euro}.{cents:02}"
    else:
        return f"€ {euro}"


def price_range_string(price_range, include_upper=False):
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
    return filter(lambda x: x is not None, iterable)
