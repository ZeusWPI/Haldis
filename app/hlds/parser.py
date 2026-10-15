#!/usr/bin/env python3

import itertools
import sys
from copy import deepcopy
from glob import glob
from os import path
import traceback
import requests
from sqlalchemy.dialects.oracle import dictionary

from app.config import Configuration
from typing import Iterable, List, Tuple, Union
import json

from tatsu import parse as tatsu_parse
from tatsu.ast import AST
from tatsu.exceptions import SemanticError
from ..utils import first

from .models import Choice, Dish, Location, Option

# TODO Use proper way to get resources, see https://stackoverflow.com/a/10935674
with open(path.join(path.dirname(__file__), "hlds.tatsu")) as fh:
    GRAMMAR = fh.read()


def filter_instance(cls, iterable):
    return [item for item in iterable if isinstance(item, cls)]


class ChoiceReference:
    def __init__(self, identifier, price):
        self.identifier = identifier
        self.price = price


# pylint: disable=no-self-use
class HldsSemanticActions:
    def location(self, ast) -> Location:
        attributes = {att["key"]: att["value"] for att in ast["attributes"]}

        choices = {
            choice.id: choice for choice in filter_instance(Choice, ast["items_"])
        }
        dishes: Iterable[Dish] = filter_instance(Dish, ast["items_"])
        for dish in dishes:
            for i, choice in enumerate(dish.choices):
                if not isinstance(choice[1], Choice):
                    choiceId, choiceRef = choice
                    assert isinstance(choiceRef, ChoiceReference)
                    # We must replace the ChoiceReference with the Choice it refers to. A deep copy
                    # allows us to modify the individual Options of the Choice.
                    choiceObject = deepcopy(choices[choiceRef.identifier])

                    for option in choiceObject.options:
                        option.price += choiceRef.price

                    dish.choices[i] = (choiceId, choiceObject)

            # Move the base price to the first single_choice if the dish doesn't have a fixed price
            first_single_choice = first(
                c[1] for c in dish.choices if c[0] == "single_choice"
            )
            price_range = dish.price_range()
            if dish.price and price_range[0] != price_range[1] and first_single_choice:
                for option in first_single_choice.options:
                    option.price += dish.price
                dish.price = 0
        dishes = list(dishes)

        if attributes.get("free_choice", "yes") != "no":
            dishes.append(
                Dish(
                    "custom",
                    name="Vrije keuze",
                    description="Zet wat je wil in comment",
                    price=0,
                    tags=[],
                    choices=[],
                )
            )

        return Location(
            ast["id"],
            name=ast["name"],
            dishes=dishes,
            osm=attributes.get("osm"),
            address=attributes.get("address"),
            telephone=attributes.get("phone"),
            website=attributes.get("website"),
        )

    def dish_block(self, ast) -> Dish:
        return Dish(
            ast["id"],
            name=ast["name"],
            description=ast["description"],
            price=ast["price"] or 0,
            tags=ast["tags"] or [],
            choices=ast["choices"],
        )

    def choice_block(self, ast) -> Choice:
        if ast["price"] or ast["tags"]:
            raise SemanticError(
                "Choice block definitions cannot have price or tags, put them on each of its options instead"
            )

        return Choice(
            ast["id"],
            name=ast["name"],
            description=ast["description"],
            options=ast["entries"],
        )

    def indent_choice_block(self, ast) -> Tuple[str, Union[Choice, AST]]:
        if ast["kind"] == "declaration":
            return (ast["type"], self.choice_block(ast))
        else:
            if ast["type"] == "single_choice" and ast["price"]:
                raise SemanticError(
                    "Single_choice choices can't have a price, because it would always be triggered"
                )
            return (ast["type"], ChoiceReference(ast["id"], ast["price"] or 0))

    def indent_choice_entry(self, ast) -> Option:
        return Option(
            ast["id"],
            name=ast["name"],
            description=ast["description"],
            price=ast["price"] or 0,
            tags=ast["tags"] or [],
        )

    noindent_choice_entry = indent_choice_entry

    def price(self, ast) -> int:
        return 100 * int(ast["value_unit"]) + (
            0
            if not ast["value_cents"]
            else (
                10 * int(ast["value_cents"])
                if len(ast["value_cents"]) == 1
                else int(ast["value_cents"])
            )
        )

    def _default(self, ast):
        return ast


SEMANTICS = HldsSemanticActions()


def parse(menu: str) -> List[Location]:
    parsed = tatsu_parse(GRAMMAR, menu, semantics=SEMANTICS)
    return parsed


def parse_file(filename: str) -> List[Location]:
    with open(filename) as file_handle:
        try:
            location = parse(file_handle.read())
        except Exception as e:
            print(traceback.format_exc())
            print(f"Error parsing {filename}: {e}, skipping")
            return []

    return location


def parse_files(files: Iterable[str]) -> List[Location]:
    menus = map(parse_file, files)
    return list(itertools.chain.from_iterable(menus))


def parse_all_directory(directory: str) -> List[Location]:
    r = requests.get(Configuration.HAM_URL + "/api/menu")
    if r.status_code != 200:
        print(f"Failed to fetch menus from HAM: {r}", file=sys.stderr)
    menus = json.loads(r.content)
    locations = []
    for menu in menus:
        r2 = requests.get(Configuration.HAM_URL + "/api/menu/" + menu)
        if r2.status_code != 200:
            print(f"Failed to fetch {menu} menu from HAM: {r}", file=sys.stderr)
            continue
        jsonmenu = json.loads(r2.content)
        jsondish = jsonmenu["dishes"]
        common_choices = jsonmenu["common_choices"]
        dishes = [
            Dish(
                jsondish[i]["id"],
                name=jsondish[i]["name"],
                description=jsondish[i]["description"],
                price=jsondish[i]["price"],
                choices=get_choices(common_choices, jsondish[i]["choices"]),
                tags=get_tags(i, jsondish)
            ) for i in range(len(jsonmenu["dishes"]))
        ]
        menu2 = Location(
            jsonmenu["id"],
            name=jsonmenu["name"],
            dishes=dishes,
            osm=jsonmenu["osm"]
        )
        locations.append(menu2)
    return locations
    # TODO Use proper way to get resources, see https://stackoverflow.com/a/10935674
    #files = glob(path.join(directory, "**.hlds"), recursive=True)
    #return parse_files(files)


def get_id(common_choice):
    return common_choice["id"]


def get_common_choice(id, commonchoices):
    choice = list(filter(lambda a: id == get_id(a), commonchoices))
    return choice[0]


def get_choices(common_choices, choice_selections) -> List[Choice]:
    retchoices = []
    for c in choice_selections:
        common_choice = get_common_choice(c["id"], common_choices)
        retchoices.append(("multi_choice" if common_choice["multiple_choice"] else "single_choice", Choice(
                                c["id"],
                                name=common_choice["name"],
                                description="",
                                options=[
                                    Option(
                                        name=option["name"],
                                        price=option["price"],
                                        description="",
                                        tags=[],
                                        id_=option["name"]
                                    ) for option in common_choice["options"]
                                ]
                            )
                           ))
    return retchoices


def get_tags(index, jsondish) -> List[str]:
    tabs = []
    if jsondish[index]["is_vegan"]:
        tabs.append("vegan")
    if jsondish[index]["is_vegetarian"]:
        tabs.append("vegetarian")
    if jsondish[index]["is_glutenfree"]:
        tabs.append("glutenfree")
    return tabs
