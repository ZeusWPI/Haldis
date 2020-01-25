#!/usr/bin/env python3

from glob import glob
from os import path, walk
from tatsu import parse as tatsu_parse
import itertools
from .models import Location


# TODO Use proper way to get resources, see https://stackoverflow.com/a/10935674
with open(path.join(path.dirname(__file__), "hlds.tatsu")) as fh:
    GRAMMAR = fh.read()


def kind_equal_to(compare_to):
    return lambda item: item["kind"] == compare_to


def parse(menu):
    parsed = tatsu_parse(GRAMMAR, menu)
    return parsed
    return dict((
        *((att["key"], att["value"]) for att in parsed["attributes"]),
        ("id",      parsed["id"]),
        ("name",    parsed["name"]),
        ("choices", (kind_equal_to("choice_declaration"), parsed["items_"])),
        ("bases",   (kind_equal_to("base"),               parsed["items_"])),
    ))


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
