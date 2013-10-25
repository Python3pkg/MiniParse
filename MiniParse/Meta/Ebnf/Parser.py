# -*- coding: utf-8 -*-

# Copyright 2013 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of MiniParse. http://jacquev6.github.com/MiniParse

# MiniParse is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# MiniParse is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with MiniParse.  If not, see <http://www.gnu.org/licenses/>.

import MiniParse
from MiniParse import LiteralParser, SequenceParser, AlternativeParser, OptionalParser, RepetitionParser

import Tokens as Tok
from NonTerminals import *


class TransformingParser:  # Temporary class to TDD the parser
    def __init__(self, parser, match):
        self.__parser = parser
        self.__match = match

    def apply(self, cursor):
        with cursor.backtracking as bt:
            if self.__parser.apply(cursor):
                return bt.success(self.__match(cursor.value))
            else:
                return bt.failure()


class ClassParser:
    def __init__(self, class_, match):
        self.__class = class_
        self.__match = match

    def apply(self, cursor):
        with cursor.backtracking as bt:
            if cursor.finished or not isinstance(cursor.current, self.__class):
                return bt.expected(self.__class.__name__)
            else:
                m = cursor.current
                cursor.advance()
                return bt.success(self.__match(m))


class Parser:
    defining = LiteralParser(Tok.Defining)
    metaIdentifier = ClassParser(Tok.MetaIdentifier, lambda name: " ".join(name.value))
    terminal = ClassParser(Tok.Terminal, lambda t: Terminal(t.value))
    terminator = LiteralParser(Tok.Terminator)

    singleDefinition = terminal

    # 4.4
    definitionsList = SequenceParser(
        [
            singleDefinition,
            RepetitionParser(
                SequenceParser(
                    [LiteralParser(Tok.DefinitionSeparator), singleDefinition],
                    lambda s, d: d
                )
            )
        ],
        lambda d1, ds: d1 if len(ds) == 0 else DefinitionsList([d1] + ds)
    )

    # 4.3
    syntaxRule = SequenceParser(
        [metaIdentifier, defining, definitionsList, terminator],
        lambda name, defining, value, terminator: SyntaxRule(name, value)
    )

    # 4.2
    syntax = RepetitionParser(syntaxRule, Syntax)

    def __call__(self, tokens):
        try:
            return MiniParse.parse(self.syntax, tokens)
        except MiniParse.SyntaxError, e:
            print "Expected", " or ".join(str(x) for x in e.expected)
            print "Here:", tokens[e.position:], ">>>", tokens[e.position], "<<<", tokens[e.position + 1]
