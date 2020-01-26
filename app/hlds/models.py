#!/usr/bin/env python3
# pylint: disable=too-few-public-methods

from typing import Iterable, List, Mapping, Any


def _format_tags(tags: Iterable[str]) -> str:
    return (
        " :: {}".format(" ".join(["{" + tag + "}" for tag in tags]))
        if tags else
        ""
    )


def _format_price(price: int) -> str:
    return " € {}.{:02}".format(*divmod(price, 100)) if price else ""


def _format_type_and_choice(type_and_choice):
    type_, choice = type_and_choice
    return "{} {}".format(type_, choice)


class Option:
    def __init__(self, id_, *, name, description, price, tags):
        self.id: str = id_
        self.name: str = name
        self.description: str = description
        self.price: int = price
        self.tags: List[str] = tags

    def __str__(self):
        return "{0.id}: {0.name}{1}{2}{3}".format(
            self,
            " -- {}".format(self.description) if self.description else "",
            _format_tags(self.tags),
            _format_price(self.price)
        )


class Choice:
    def __init__(self, id_, *, name, description, options):
        self.id: str = id_
        self.name: str = name
        self.description: str = description

        self.options: List[Option] = options

    def __str__(self):
        return "{0.id}: {0.name}{1}\n\t\t{2}".format(
            self,
            " -- {}".format(self.description) if self.description else "",
            "\n\t\t".join(map(str, self.options))
        )


class Dish:
    def __init__(self, id_, *, name, description, price, tags, choices):
        self.id: str = id_
        self.name: str = name
        self.description: str = description
        self.price: int = price
        self.tags: List[str] = tags

        self.choices: List[(str, Choice)] = choices

    def __str__(self):
        return "base {0.id}: {0.name}{1}{2}{3}\n\t{4}".format(
            self,
            " -- {}".format(self.description) if self.description else "",
            _format_tags(self.tags),
            _format_price(self.price),
            "\n\t".join(map(_format_type_and_choice, self.choices))
        )


class Location:
    def __init__(self, id_, *, name, attributes, dishes):
        self.id: str = id_
        self.name: str = name
        self.attributes: Mapping[str, Any] = attributes

        self.dishes: List[Dish] = dishes

    def __str__(self):
        return (
            "============================\n"
            "{0.id}: {0.name}\n"
            "============================\n"
            "\n"
            "{1}"
        ).format(
            self,
            "\n".join(map(str, self.dishes))
        )
