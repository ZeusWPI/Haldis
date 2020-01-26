#!/usr/bin/env python3

from glob import glob
from os import path, walk
from tatsu import parse as tatsu_parse
import itertools
from .models import Location, Choice, Option, Dish
import operator


# TODO Use proper way to get resources, see https://stackoverflow.com/a/10935674
with open(path.join(path.dirname(__file__), "hlds.tatsu")) as fh:
    GRAMMAR = fh.read()


def filter_instance(cls, iterable):
    return [item for item in iterable if isinstance(item, cls)]


class HldsSemanticActions:
    def location(self, ast):
        return Location(
            ast["id"],
            name=ast["name"],
            attributes={att["key"]: att["value"] for att in ast["attributes"]},
            dishes=filter_instance(Dish, ast["items_"]),
        )

    def base_block(self, ast):
        return Dish(
            ast["id"],
            name=ast["name"],
            description=ast["description"],
            price=ast["price"],
            tags=ast["tags"] if ast["tags"] else [],
            choices=ast["choices"],
        )

    def choice_block(self, ast):
        return Choice(
            ast["id"],
            name=ast["name"],
            description=ast["description"],
            options=ast["entries"],
        )

    def indent_choice_block(self, ast):
        if ast["kind"] == "declaration":
            return self.choice_block(ast)
        else:
            return ast

    def indent_choice_entry(self, ast):
        return Option(
            ast["id"],
            name=ast["name"],
            description=ast["description"],
            price=ast["price"],
            tags=ast["tags"],
        )

    def price(self, ast):
        return "{0[currency]} {0[value]}".format(ast)

    def _default(self, ast):
        return ast

SEMANTICS = HldsSemanticActions()


def parse(menu):
    parsed = tatsu_parse(GRAMMAR, menu, semantics=SEMANTICS)
    return parsed


def parse_file(filename):
    with open(filename, "r") as fh:
        return parse(fh.read())


def parse_files(files):
    menus = map(parse_file, files)
    return list(itertools.chain.from_iterable(menus))


def parse_all_directory(directory):
    # TODO Use proper way to get resources, see https://stackoverflow.com/a/10935674
    files = glob(path.join(directory, "**.hlds"), recursive=True)
    return parse_files(files)
