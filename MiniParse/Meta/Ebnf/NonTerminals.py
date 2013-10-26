# -*- coding: utf-8 -*-

# Copyright 2013 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of MiniParse. http://jacquev6.github.com/MiniParse

# MiniParse is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# MiniParse is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with MiniParse.  If not, see <http://www.gnu.org/licenses/>.


class _deepComparable:
    def __eq__(self, other):
        return other.__class__ is self.__class__ and other.__dict__ == self.__dict__


class Syntax(_deepComparable):
    def __init__(self, rules):
        self.__rules = rules

    def generateMiniParser(self, computeParserName, computeMatchName):
        return (
            "from MiniParse import OptionalParser, SequenceParser, AlternativeParser, LiteralParser, RepeatedParser\n"
            + "\n"
            + "\n"
            + "".join(rule.generate(computeParserName, computeMatchName) for rule in self.__rules)
        )


class SyntaxRule(_deepComparable):
    def __init__(self, name, definition):
        self.__name = name
        self.__definition = definition

    def generate(self, computeParserName, computeMatchName):
        parserName = computeParserName(self.__name)
        matchName = computeMatchName(self.__name)
        if isinstance(self.__definition, (Terminal, NonTerminal)):  # @todo Use a virtual method...
            return parserName + " = " + self.__definition.generate() + "\n"
        else:
            return (
                "class " + parserName + ":\n"
                + "    @staticmethod\n"
                + "    def apply(cursor):\n"
                + "        return " + self.__definition.generate(", " + matchName) + ".apply(cursor)\n"
                + "\n"
                + "\n"
            )


class Sequence(_deepComparable):
    def __init__(self, terms):
        self.__terms = terms

    def generate(self, args=""):
        return "SequenceParser([" + ", ".join(t.generate() for t in self.__terms) + "]" + args + ")"


class Alternative(_deepComparable):
    def __init__(self, definitions):
        self.__definitions = definitions

    def generate(self, args=""):
        return "AlternativeParser([" + ", ".join(d.generate() for d in self.__definitions) + "]" + args + ")"


class Repetition(_deepComparable):
    def __init__(self, number, primary):
        self.__number = number
        self.__primary = primary


class Optional(_deepComparable):
    def __init__(self, definition):
        self.__definition = definition

    def generate(self, args=""):
        return "OptionalParser(" + self.__definition.generate() + args + ")"


class Repeated(_deepComparable):
    def __init__(self, definition):
        self.__definition = definition

    def generate(self, args=""):
        return "RepeatedParser(" + self.__definition.generate() + args + ")"


class Terminal(_deepComparable):
    def __init__(self, value):
        self.__value = value

    def generate(self):
        return "LiteralParser('" + self.__value + "')"


class NonTerminal(_deepComparable):
    def __init__(self, name):
        self.__name = name

    def generate(self):
        return self.__name + "Parser"


class Restriction(_deepComparable):
    def __init__(self, base, exception):
        self.__base = base
        self.__exception = exception

    def generate(self, args=""):
        return "RestrictionParser(" + self.__base.generate() + ", " + self.__exception.generate() + args + ")"
