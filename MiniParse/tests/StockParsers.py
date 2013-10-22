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
import MockMockMock

from MiniParse import parse, SyntaxError
from MiniParse import LiteralParser, SequenceParser, AlternativeParser


class ParserTestCase(unittest.TestCase):
    def expectSuccess(self, input, value):
        self.assertEqual(parse(self.p, input), value)

    def expectFailure(self, input, position, expected):
        with self.assertRaises(SyntaxError) as cm:
            parse(self.p, input)
        self.assertEqual(cm.exception.position, position)
        self.assertEqual(cm.exception.expected, set(expected))


class Literal(ParserTestCase):
    def setUp(self):
        self.p = LiteralParser(42)

    def testSuccess(self):
        self.expectSuccess([42], 42)

    def testFailure(self):
        self.expectFailure([41], 0, [42])

    def testPartialSuccess(self):
        self.expectFailure([42, 43], 1, [])


class Sequence(ParserTestCase):
    def setUp(self):
        self.p = SequenceParser([
            LiteralParser(42),
            LiteralParser(43),
            LiteralParser(44),
            LiteralParser(45)
        ])

    def testSuccess(self):
        self.expectSuccess([42, 43, 44, 45], (42, 43, 44, 45))

    def testFailure1(self):
        self.expectFailure([41], 0, [42])

    def testFailure2(self):
        self.expectFailure([42, 41], 1, [43])

    def testFailure3(self):
        self.expectFailure([42, 43, 41], 2, [44])

    def testFailure4(self):
        self.expectFailure([42, 43, 44, 41], 3, [45])

    def testPartialSuccess(self):
        self.expectFailure([42, 43, 44, 45, 46], 4, [])


class UnambiguousAlternative(ParserTestCase):
    def setUp(self):
        self.p = AlternativeParser([
            SequenceParser([LiteralParser(42), LiteralParser(43)]),
            SequenceParser([LiteralParser(44), LiteralParser(45)]),
            SequenceParser([LiteralParser(46), LiteralParser(47)])
        ])

    def testSuccess1(self):
        self.expectSuccess([42, 43], (42, 43))

    def testSuccess2(self):
        self.expectSuccess([44, 45], (44, 45))

    def testSuccess3(self):
        self.expectSuccess([46, 47], (46, 47))

    def testFailure0(self):
        self.expectFailure([41], 0, [42, 44, 46])

    def testFailure1(self):
        self.expectFailure([42, 41], 1, [43])

    def testFailure2(self):
        self.expectFailure([44, 41], 1, [45])

    def testFailure3(self):
        self.expectFailure([46, 41], 1, [47])

    def testPartialSuccess1(self):
        self.expectFailure([42, 43, 41], 2, [])

    def testPartialSuccess2(self):
        self.expectFailure([44, 45, 41], 2, [])

    def testPartialSuccess3(self):
        self.expectFailure([46, 47, 41], 2, [])
