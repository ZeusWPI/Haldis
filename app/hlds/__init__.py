#!/usr/bin/env python3

from glob import glob
from os import path, walk
from tatsu import parse as tatsu_parse
import itertools


# TODO Use proper way to get resources, see https://stackoverflow.com/a/10935674
with open(path.join(path.dirname(__file__), "hlds.tatsu")) as fh:
    GRAMMAR = fh.read()


def kind_comparer(compare_to):
    return lambda item: item["kind"] == compare_to


def parse(menu):
    parsed = tatsu_parse(GRAMMAR, menu)
    return parsed
    return dict((
        *((att["key"], att["value"]) for att in parsed["attributes"]),
        ("id",      parsed["id"]),
        ("name",    parsed["name"]),
        ("choices", filter(kind_comparer("choice_declaration"), parsed["items_"])),
        ("bases",   filter(kind_comparer("base"),               parsed["items_"])),
    ))


def parse_file(filename):
    with open(filename, "r") as fh:
        return parse(fh.read())


def load_all():
    # TODO Use proper way to get resources, see https://stackoverflow.com/a/10935674
    data_dir = path.join(path.dirname(__file__), "..", "..", "data")
    files = glob(path.join(data_dir, "**.hlds"))
    menus = map(parse_file, files)
    return list(itertools.chain.from_iterable(menus))


def main(filename):
    import json
    from tatsu.util import asjson

    ast = parse_file(filename)
    print(json.dumps(asjson(ast), indent="\t"))


if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])
