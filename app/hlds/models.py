#!/usr/bin/env python3

from typing import List


class Option:
    def __init__(self, id_, name, description):
        self.id = id_
        self.name = name
        self.description = description


class Choice:
    def __init__(self, id_, name, description, options):
        self.id = id_
        self.name = name
        self.description = description

        self.options: List[Option] = options


class Location:
    def __init__(self, id_, name, properties, choices, bases):
        self.id = id_
        self.name = name
        self.properties = properties

        self.choices: List[Choice] = choices
        self.bases = bases
