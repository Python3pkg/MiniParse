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

# Rewrite: should not change
from MiniParse import OptionalParser, SequenceParser, AlternativeParser, LiteralParser, RepetitionParser
# Rewrite: will change
from MiniParse import Cursor


# Rewrite: will change
class ParserTestCase(unittest.TestCase):
    def expectParsingFailure(self, input, position, expected):
        r = self.p.parse(Cursor(input))
        self.assertFalse(r.ok)
        self.assertEqual(r.position, position)
        self.assertEqual(r.expected, set(expected))

    def expectParsingSuccess(self, input, value, position, expected):
        r = self.p.parse(Cursor(input))
        self.assertTrue(r.ok)
        self.assertEqual(r.value, value)
        self.assertEqual(r.failure.position, position)
        self.assertEqual(r.failure.expected, set(expected))


# Rewrite: should not change
class ErrorHandling(ParserTestCase):
    def testErrorComesFromFirstLongestAlternative(self):
        self.p = AlternativeParser([
            LiteralParser("abx"),
            LiteralParser("abcy"),
            LiteralParser("abcw"),
            LiteralParser("az")
        ])
        self.expectParsingFailure("abcd", 3, ["'abcy'", "'abcw'"])

    def testLiteralParserTellsWhereItFailed(self):
        self.p = LiteralParser("abcy")
        self.expectParsingFailure("abcd", 3, ["'abcy'"])

    def testOptionalParserTellsIfSomethingCouldHaveBeenBetter(self):
        self.p = OptionalParser(LiteralParser("abcy"))
        self.expectParsingSuccess("abcd", None, 3, ["'abcy'"])

    def testSequenceStartingWithOptional(self):
        self.p = SequenceParser([
            OptionalParser(LiteralParser("abcy")),
            LiteralParser("az")
        ])
        self.expectParsingFailure("abcd", 3, ["'abcy'"])

    def testSequenceParserTellsIfSomethingCouldHaveBeenBetter(self):
        self.p = SequenceParser([
            OptionalParser(LiteralParser("abcy")),
            LiteralParser("ab")
        ])
        self.expectParsingSuccess("abcd", (None, "ab"), 3, ["'abcy'"])

    def testSequenceParserTellsIfSomethingCouldHaveBeenBetter_Tie(self):
        self.p = SequenceParser([
            OptionalParser(LiteralParser("abcy")),
            LiteralParser("abcz")
        ])
        self.expectParsingFailure("abcd", 3, ["'abcz'", "'abcy'"])

    def testRepetitionParserTellsIfSomethingCouldHaveBeenBetter(self):
        self.p = RepetitionParser(
            SequenceParser([
                OptionalParser(LiteralParser("abcy")),
                LiteralParser("ab")
            ])
        )
        self.expectParsingSuccess("abcd", [(None, "ab")], 3, ["'abcy'"])

    def testRepetitionParserTellsIfSomethingCouldHaveBeenBetter_2(self):
        self.p = RepetitionParser(
            AlternativeParser([
                LiteralParser("ab"),
                LiteralParser("acd")
            ])
        )
        self.expectParsingSuccess("ababacab", ["ab", "ab"], 6, ["'acd'"])

    def testAlternativeParserGivesAllExpectedValues(self):
        self.p = AlternativeParser([
            AlternativeParser([LiteralParser("xa"), LiteralParser("xb")]),
            AlternativeParser([LiteralParser("xc"), LiteralParser("xd"), LiteralParser("z")])
        ])
        self.expectParsingFailure("xe", 1, ["'xa'", "'xb'", "'xc'", "'xd'"])
