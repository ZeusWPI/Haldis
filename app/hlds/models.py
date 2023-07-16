#!/usr/bin/env python3
# pylint: disable=too-few-public-methods

from typing import Any, Iterable, List, Mapping, Optional, Tuple

from utils import euro_string, first


def _format_tags(tags: Iterable[str]) -> str:
    # pylint: disable=consider-using-f-string
    return " :: {}".format(" ".join(["{" + tag + "}"
                                     for tag in tags])) if tags else ""


def _format_price(price: int) -> str:
    return f" {euro_string(price)}" if price else ""


def _format_type_and_choice(type_and_choice):
    type_, choice = type_and_choice
    return f"{type_} {choice}"


class Option:

    def __init__(self, id_, *, name, description, price, tags):
        self.id: str = id_
        self.name: str = name
        self.description: str = description
        self.price: int = price
        self.tags: List[str] = tags

    def __str__(self):
        # pylint: disable=consider-using-f-string
        return "{0.id}: {0.name}{1}{2}{3}".format(
            self,
            f" -- {self.description}" if self.description else "",
            _format_tags(self.tags),
            _format_price(self.price),
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
            f" -- {self.description}" if self.description else "",
            "\n\t\t".join(map(str, self.options)),
        )

    def option_by_id(self, option_id: str) -> Optional[Option]:
        return first(filter(lambda o: o.id == option_id, self.options))


class Dish:

    def __init__(self, id_, *, name, description, price, tags, choices):
        self.id: str = id_
        self.name: str = name
        self.description: str = description
        self.price: int = price
        self.tags: List[str] = tags

        # The str in (str, Choice) is the type of choice: single_choice or multi_choice
        self.choices: List[(str, Choice)] = choices

    def __str__(self):
        return "dish {0.id}: {0.name}{1}{2}{3}\n\t{4}".format(
            self,
            f" -- {self.description}" if self.description else "",
            _format_tags(self.tags),
            _format_price(self.price),
            "\n\t".join(map(_format_type_and_choice, self.choices)),
        )

    def price_range(self) -> Tuple[int, int]:
        return (
            self.price + self._sum_f_option_prices(min),
            self.price + self._sum_f_option_prices(max),
        )

    def _sum_f_option_prices(self, f):
        for (_, choice) in self.choices:
            if len(choice.options) == 0:
                print((f"[PARSE ERROR] At least 1 option expected in dish choice.\n"
                       f"\tDish:\t'{self.name}'\n"
                       f"\tChoice:\t'{choice.name}'\n"))
                exit(1)
        return sum(
            f(option.price for option in choice.options)
            for (choice_type, choice) in self.choices
            if choice_type == "single_choice")


class Location:

    def __init__(self,
                 id_,
                 *,
                 name,
                 dishes,
                 osm=None,
                 address=None,
                 telephone=None,
                 website=None):
        self.id: str = id_
        self.name: str = name
        self.osm: Optional[str] = osm
        self.address: Optional[str] = address
        self.telephone: Optional[str] = telephone
        self.website: Optional[str] = website

        self.dishes: List[Dish] = dishes

    def dish_by_id(self, dish_id: str) -> Optional[Dish]:
        return first(filter(lambda d: d.id == dish_id, self.dishes))

    def __str__(self):
        return ("============================\n"
                "{0.id}: {0.name}"
                "{1}\n"
                "============================\n"
                "\n"
                "{2}").format(
                    self,
                    "".join(f"\n\t{k} {v}" for k, v in (
                        ("osm", self.osm),
                        ("address", self.address),
                        ("telephone", self.telephone),
                        ("website", self.website),
                    ) if v is not None),
                    "\n".join(map(str, self.dishes)),
                )
