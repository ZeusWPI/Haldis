"Script which contains several utils for Haldis"

from typing import Iterable


def euro_string(value: int) -> str:
    """
    Convert cents to string formatted euro
    """
    return "€ {}.{:02}".format(*divmod(value, 100))


def first(iterable: Iterable, default=None):
    """
    Return first element of iterable
    """
    try:
        return next(iter(iterable))
    except StopIteration:
        return default

