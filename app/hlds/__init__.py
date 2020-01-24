#!/usr/bin/env python3

from os import path
from tatsu import parse as tatsu_parse


# TODO Use proper way to get resources, see https://stackoverflow.com/a/10935674
with open(path.join(path.dirname(__file__), "hlds.tatsu")) as fh:
	GRAMMAR = fh.read()


def kind_comparer(compare_to):
	return lambda item: item["kind"] == compare_to


def parse(menu):
	parsed = tatsu_parse(GRAMMAR, menu)
	return dict((
		*((att["key"], att["value"]) for att in parsed["attributes"]),
		("id",      parsed["id"]),
		("name",    parsed["name"]),
		("choices", filter(kind_comparer("choice_declaration"), parsed["items_"])),
		("bases",   filter(kind_comparer("base"),               parsed["items_"])),
	))


def main(filename):
	import json
	from tatsu.util import asjson

	with open(filename) as fh:
		ast = parse(fh.read())
	print(json.dumps(asjson(ast), indent="\t"))


if __name__ == "__main__":
	import sys
	main(*sys.argv[1:])
