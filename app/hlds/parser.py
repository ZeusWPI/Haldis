#!/usr/bin/env python3

from glob import glob
from os import path
import itertools
from typing import Iterable, List, Union, Tuple
from tatsu import parse as tatsu_parse
from tatsu.ast import AST
from .models import Location, Choice, Option, Dish


# TODO Use proper way to get resources, see https://stackoverflow.com/a/10935674
with open(path.join(path.dirname(__file__), "hlds.tatsu")) as fh:
    GRAMMAR = fh.read()


def filter_instance(cls, iterable):
    return [item for item in iterable if isinstance(item, cls)]


# pylint: disable=no-self-use
class HldsSemanticActions:
    def location(self, ast) -> Location:
        choices = {choice.id: choice for choice in filter_instance(Choice, ast["items_"])}
        dishes = filter_instance(Dish, ast["items_"])
        for dish in dishes:
            for i, choice in enumerate(dish.choices):
                if not isinstance(choice[1], Choice):
                    dish.choices[i] = (dish.choices[i][0], choices[choice[1]])

        attributes = {att["key"]: att["value"] for att in ast["attributes"]}

        return Location(
            ast["id"],
            name=ast["name"],
            dishes=dishes,
            osm=attributes.get("osm"),
            address=attributes.get("address"),
            telephone=attributes.get("telephone"),
            website=attributes.get("website"),
        )

    def dish_block(self, ast) -> Dish:
        return Dish(
            ast["id"],
            name=ast["name"],
            description=ast["description"],
            price=ast["price"] if ast["price"] else 0,
            tags=ast["tags"] if ast["tags"] else [],
            choices=ast["choices"],
        )

    def choice_block(self, ast) -> Choice:
        return Choice(
            ast["id"],
            name=ast["name"],
            description=ast["description"],
            options=ast["entries"],
        )

    def indent_choice_block(self, ast) -> Tuple[str, Union[Choice, AST]]:
        return (
            (ast["type"], self.choice_block(ast))
            if ast["kind"] == "declaration" else
            (ast["type"], ast["id"])
        )

    def indent_choice_entry(self, ast) -> Option:
        return Option(
            ast["id"],
            name=ast["name"],
            description=ast["description"],
            price=ast["price"] if ast["price"] else 0,
            tags=ast["tags"],
        )

    noindent_choice_entry = indent_choice_entry

    def price(self, ast) -> int:
        return (
            100 * int(ast["value_unit"]) +
            (
                0 if not ast["value_cents"] else
                10 * int(ast["value_cents"]) if len(ast["value_cents"]) == 1 else
                int(ast["value_cents"])
            )
        )

    def _default(self, ast):
        return ast

SEMANTICS = HldsSemanticActions()


def parse(menu: str) -> List[Location]:
    parsed = tatsu_parse(GRAMMAR, menu, semantics=SEMANTICS)
    return parsed


def parse_file(filename: str) -> List[Location]:
    with open(filename, "r") as file_handle:
        return parse(file_handle.read())


def parse_files(files: Iterable[str]) -> List[Location]:
    menus = map(parse_file, files)
    return list(itertools.chain.from_iterable(menus))


def parse_all_directory(directory: str) -> List[Location]:
    # TODO Use proper way to get resources, see https://stackoverflow.com/a/10935674
    files = glob(path.join(directory, "**.hlds"), recursive=True)
    return parse_files(files)
