# -*- coding: utf-8 -*-

# Copyright 2013 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of MiniParse. http://jacquev6.github.com/MiniParse

# MiniParse is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# MiniParse is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with MiniParse.  If not, see <http://www.gnu.org/licenses/>.


class Syntax:
    def __init__(self, rules):
        self.__rules = rules

    def generateMiniParser(self, mainRule, computeParserName, computeMatchName):
        return (
            "class Parser:\n"
            + "    def __call__(self, tokens):\n"
            + "\n".join(rule.generate(computeParserName, computeMatchName) for rule in self.__rules)
            + "\n"
            + "        return MiniParse.parse(" + computeParserName(mainRule) + ", tokens)\n"
        )


class Rule:
    def __init__(self, name, definition):
        self.__name = name
        self.__definition = definition

    def generate(self, computeParserName, computeMatchName):
        parserName = computeParserName(self.__name)
        matchName = computeMatchName(self.__name)
        if isinstance(self.__definition, (Terminal, NonTerminal)):  # @todo Use a virtual method...
            return "        " + parserName + " = " + self.__definition.generate(computeParserName) + "\n"
        else:
            return (
                "        class " + parserName + ":\n"
                + "            @staticmethod\n"
                + "            def apply(cursor):\n"
                + "                return " + self.__definition.generate(computeParserName, ", " + matchName) + ".apply(cursor)\n"
            )


class Sequence:
    def __init__(self, terms):
        self.__terms = terms

    def generate(self, computeParserName, args=""):
        return "MiniParse.SequenceParser([" + ", ".join(t.generate(computeParserName) for t in self.__terms) + "]" + args + ")"


class Alternative:
    def __init__(self, definitions):
        self.__definitions = definitions

    def generate(self, computeParserName, args=""):
        return "MiniParse.AlternativeParser([" + ", ".join(d.generate(computeParserName) for d in self.__definitions) + "]" + args + ")"


class Optional:
    def __init__(self, definition):
        self.__definition = definition

    def generate(self, computeParserName, args=""):
        return "MiniParse.OptionalParser(" + self.__definition.generate(computeParserName) + args + ")"


class Repeated:
    def __init__(self, definition):
        self.__definition = definition

    def generate(self, computeParserName, args=""):
        return "MiniParse.RepeatedParser(" + self.__definition.generate(computeParserName) + args + ")"


class Terminal:
    def __init__(self, value):
        self.__value = value

    def generate(self, computeParserName):
        return "MiniParse.LiteralParser(" + repr(self.__value) + ")"


class NonTerminal:
    def __init__(self, name):
        self.__name = name

    def generate(self, computeParserName):
        return computeParserName(self.__name)


class Restriction:
    def __init__(self, base, exception):
        self.__base = base
        self.__exception = exception

    def generate(self, computeParserName, args=""):
        return "MiniParse.RestrictionParser(" + self.__base.generate(computeParserName) + ", " + self.__exception.generate(computeParserName) + args + ")"


class Repetition:
    def __init__(self, n, base):
        self.__n = n
        self.__base = base

    def generate(self, computeParserName, args=""):
        return "MiniParse.RepetitionParser(" + str(self.__n) + ", " + self.__base.generate(computeParserName) + args + ")"
