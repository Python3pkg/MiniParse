# -*- coding: utf-8 -*-

# Copyright 2013 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of MiniParse. http://jacquev6.github.com/MiniParse

# MiniParse is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# MiniParse is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with MiniParse.  If not, see <http://www.gnu.org/licenses/>.

import unittest

from MiniParse import LiteralParser, SequenceParser, AlternativeParser, OptionalParser, RepetitionParser
from Framework import ParserTestCase


class CustomizedExpected(ParserTestCase):
    def testLiteralParser1(self):
        self.p = LiteralParser(42, "expected")
        self.expectFailure([], 0, ["expected"])

    def testLiteralParser2(self):
        self.p = LiteralParser(42, "expected")
        self.expectFailure([41], 0, ["expected"])

    def testAlternativeParser1(self):
        self.p = AlternativeParser([LiteralParser(42), LiteralParser(43)], "expected")
        self.expectFailure([], 0, ["expected"])

    def testAlternativeParser2(self):
        self.p = AlternativeParser([LiteralParser(42), LiteralParser(43)], "expected")
        self.expectFailure([41], 0, ["expected"])

    def testSequenceParser1(self):
        self.p = SequenceParser([LiteralParser(42), LiteralParser(43)], "expected")
        self.expectFailure([], 0, ["expected"])

    def testSequenceParser2(self):
        self.p = SequenceParser([LiteralParser(42), LiteralParser(43)], "expected")
        self.expectFailure([41], 0, ["expected"])

    def testSequenceParser3(self):
        self.p = SequenceParser([LiteralParser(42), LiteralParser(43)], "expected")
        self.expectFailure([42], 0, ["expected"])

    def testSequenceParser4(self):
        self.p = SequenceParser([LiteralParser(42), LiteralParser(43)], "expected")
        self.expectFailure([42, 41], 0, ["expected"])


class ImbricatedCustomizedExpected(ParserTestCase):
    def setUp(self):
        self.p = SequenceParser(
            [
                LiteralParser('"', "opening quote"),
                RepetitionParser(AlternativeParser(
                    [
                        LiteralParser("a", "A"),
                        LiteralParser("b", "B"),
                    ],
                    "char"
                )),
                LiteralParser('"', "closing quote"),
            ],
            "string"
        )

    def testAsIs(self):
        self.expectFailure('', 0, ["string"])
        self.expectFailure('"abba', 0, ["string"])
        self.expectFailure('"abbax', 0, ["string"])

    def testWithoutString(self):
        self.p._SequenceParser__expected = None
        self.expectFailure('"abba', 5, ["closing quote", "char"])
        self.expectFailure('"abbax', 5, ["closing quote", "char"])

    def testWithOnlyLiterals(self):
        self.p._SequenceParser__expected = None
        self.p._SequenceParser__elements[1]._RepetitionParser__parser._AlternativeParser__expected = None
        self.expectFailure('', 0, ["opening quote"])
        self.expectFailure('"abba', 5, ["A", "B", "closing quote"])
        self.expectFailure('"abbax', 5, ["A", "B", "closing quote"])

    def testWithOnlyAlternative(self):
        self.p._SequenceParser__expected = None
        self.p._SequenceParser__elements[0]._LiteralParser__expected = None
        self.p._SequenceParser__elements[1]._RepetitionParser__parser._AlternativeParser__elements[0]._LiteralParser__expected = None
        self.p._SequenceParser__elements[1]._RepetitionParser__parser._AlternativeParser__elements[1]._LiteralParser__expected = None
        self.p._SequenceParser__elements[2]._LiteralParser__expected = None
        self.expectFailure('', 0, ['"'])
        self.expectFailure('"abba', 5, ["char", '"'])
        self.expectFailure('"abbax', 5, ["char", '"'])

    def testWithoutAnything(self):
        self.p._SequenceParser__expected = None
        self.p._SequenceParser__elements[0]._LiteralParser__expected = None
        self.p._SequenceParser__elements[1]._RepetitionParser__parser._AlternativeParser__expected = None
        self.p._SequenceParser__elements[1]._RepetitionParser__parser._AlternativeParser__elements[0]._LiteralParser__expected = None
        self.p._SequenceParser__elements[1]._RepetitionParser__parser._AlternativeParser__elements[1]._LiteralParser__expected = None
        self.p._SequenceParser__elements[2]._LiteralParser__expected = None
        self.expectFailure('', 0, ['"'])
        self.expectFailure('"abba', 5, ["a", "b", '"'])
        self.expectFailure('"abbax', 5, ["a", "b", '"'])
