#!/usr/bin/env python3

from os import path
from tatsu import parse as tatsu_parse


# TODO Use proper way to get resources, see https://stackoverflow.com/a/10935674
with open(path.join(path.dirname(__file__), "hlds.tatsu")) as fh:
	GRAMMAR = fh.read()


def parse(menu):
	return tatsu_parse(GRAMMAR, menu)


def main(filename):
	import json
	from tatsu.util import asjson

	with open(filename) as fh:
		ast = parse(fh.read())
	print(json.dumps(asjson(ast), indent="\t"))


if __name__ == "__main__":
	import sys
	main(*sys.argv[1:])
