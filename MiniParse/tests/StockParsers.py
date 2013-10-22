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
from MiniParse import LiteralParser, SequenceParser


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
