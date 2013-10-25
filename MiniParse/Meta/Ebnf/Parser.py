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
from MiniParse import LiteralParser, SequenceParser, AlternativeParser, OptionalParser, RepeatedParser

import Tokens as Tok
from NonTerminals import *


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


# See http://www.cl.cam.ac.uk/~mgk25/iso-14977.pdf
class Parser:
    # 4.21
    emptySequence = SequenceParser([], lambda: Empty())

    # 4.16
    terminal = ClassParser(Tok.Terminal, lambda t: Terminal(t.value))

    # 4.14
    metaIdentifier = ClassParser(Tok.MetaIdentifier, lambda name: " ".join(name.value))
    nonTerminal = ClassParser(Tok.MetaIdentifier, lambda name: NonTerminal(" ".join(name.value)))

    # 4.13
    class groupedSequence:
        @staticmethod
        def apply(cursor):
            return SequenceParser(
                [
                    LiteralParser(Tok.StartGroup),
                    Parser.definitionsList,
                    LiteralParser(Tok.EndGroup)
                ],
                lambda s, d, e: d
            ).apply(cursor)

    # 4.12
    class repeatedSequence:
        @staticmethod
        def apply(cursor):
            return SequenceParser(
                [
                    LiteralParser(Tok.StartRepeat),
                    Parser.definitionsList,
                    LiteralParser(Tok.EndRepeat)
                ],
                lambda s, d, e: Repeated(d)
            ).apply(cursor)

    # 4.11
    class optionalSequence:
        @staticmethod
        def apply(cursor):
            return SequenceParser(
                [
                    LiteralParser(Tok.StartOption),
                    Parser.definitionsList,
                    LiteralParser(Tok.EndOption)
                ],
                lambda s, d, e: Optional(d)
            ).apply(cursor)

    # 4.10
    syntacticPrimary = AlternativeParser(
        [
            optionalSequence,
            repeatedSequence,
            groupedSequence,
            nonTerminal,
            terminal,
            # specialSequence,  # @todo Implement
            emptySequence
        ]
    )

    # 4.9
    integer = ClassParser(Tok.Integer, lambda i: i.value)

    # 4.8
    syntacticFactor = AlternativeParser(
        [
            SequenceParser(
                [integer, LiteralParser(Tok.Repetition), syntacticPrimary],
                lambda i, rep, p: Repetition(i, p)
            ),
            syntacticPrimary
        ]
    )

    # 4.7
    syntacticException = syntacticFactor

    # 4.6 and 4.7
    syntacticTerm = AlternativeParser(
        [
            SequenceParser(
                [
                    syntacticFactor,
                    LiteralParser(Tok.Except),
                    syntacticException
                ],
                lambda a, e, b: Restriction(a, b)
            ),
            syntacticFactor
        ]
    )

    # 4.5
    singleDefinition = SequenceParser(
        [
            syntacticTerm,
            RepeatedParser(
                SequenceParser(
                    [LiteralParser(Tok.Concatenate), syntacticTerm],
                    lambda s, d: d
                )
            )
        ],
        lambda t1, ts: t1 if len(ts) == 0 else Sequence([t1] + ts)
    )

    # 4.4
    definitionsList = SequenceParser(
        [
            singleDefinition,
            RepeatedParser(
                SequenceParser(
                    [LiteralParser(Tok.DefinitionSeparator), singleDefinition],
                    lambda s, d: d
                )
            )
        ],
        lambda d1, ds: d1 if len(ds) == 0 else Alternative([d1] + ds)
    )

    # 4.3
    syntaxRule = SequenceParser(
        [metaIdentifier, LiteralParser(Tok.Defining), definitionsList, LiteralParser(Tok.Terminator)],
        lambda name, defining, value, terminator: SyntaxRule(name, value)
    )

    # 4.2
    syntax = RepeatedParser(syntaxRule, Syntax)

    def __call__(self, tokens):
        try:
            return MiniParse.parse(self.syntax, tokens)
        except MiniParse.SyntaxError, e:
            raise Exception(
                "Expected " + " or ".join(str(x) for x in e.expected),
                "Here: " + str(tokens[e.position - 10:e.position]) + " >>> " + str(tokens[e.position]) + " <<< " + str(tokens[e.position + 1:e.position + 10])
            )
