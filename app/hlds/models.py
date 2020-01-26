#!/usr/bin/env python3

from typing import List


def _format_tags(tags):
    return (
        " :: {}".format(" ".join(["{" + tag + "}" for tag in tags]))
        if tags else
        ""
    )


class Option:
    def __init__(self, id_, *, name, description, price, tags):
        self.id = id_
        self.name = name
        self.description = description
        self.price = price
        self.tags = tags

    def __str__(self):
        return "{0.id}: {0.name}{1}{2}{3}".format(
            self,
            " -- {}".format(self.description) if self.description else "",
            _format_tags(self.tags),
            " {}".format(self.price) if self.price else ""
        )


class Choice:
    def __init__(self, id_, *, name, description, options):
        self.id = id_
        self.name = name
        self.description = description

        self.options: List[Option] = options

    def __str__(self):
        return "{0.id}: {0.name}{1}\n\t\t{2}".format(
            self,
            " -- {}".format(self.description) if self.description else "",
            "\n\t\t".join(map(str, self.options))
        )


class Dish:
    def __init__(self, id_, *, name, description, price, tags, choices):
        self.id = id_
        self.name = name
        self.description = description
        self.price = price
        self.tags = tags

        self.choices: List[Choice] = choices

    def __str__(self):
        return "{0.id}: {0.name}{1}{2}{3}\n\t{4}".format(
            self,
            " -- {}".format(self.description) if self.description else "",
            _format_tags(self.tags),
            " {}".format(self.price) if self.price else "",
            "\n\t".join(map(str, self.choices))
        )


class Location:
    def __init__(self, id_, *, name, attributes, dishes):
        self.id = id_
        self.name = name
        self.attributes = attributes

        self.dishes: List[Dish] = dishes

    def __str__(self):
        return "============================\n{0.id}: {0.name}\n============================\n\n{1}".format(
            self,
            "\n\n".join(map(str, self.dishes))
        )
