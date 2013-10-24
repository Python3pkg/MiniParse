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

from MiniParse import LiteralParser, SequenceParser, AlternativeParser, OptionalParser, RepetitionParser
from Framework import ParserTestCase


class CustomizedValue(ParserTestCase):
    def setUp(self):
        self.mocks = MockMockMock.Engine()
        self.match = self.mocks.create("match")

    def tearDown(self):
        self.mocks.tearDown()

    def testLiteralParser(self):
        self.p = LiteralParser(42, match=43)
        self.expectSuccess([42], 43)

    def testAlternativeParser(self):
        self.p = AlternativeParser([LiteralParser(42), LiteralParser(43)], match=self.match.object)
        self.match.expect(42).andReturn(43)
        self.expectSuccess([42], 43)

    def testSequenceParser(self):
        self.p = SequenceParser([LiteralParser(42), LiteralParser(43)], match=self.match.object)
        self.match.expect((42, 43)).andReturn(45)
        self.expectSuccess([42, 43], 45)

    def testOptionalParser(self):
        self.p = OptionalParser(LiteralParser(42), match=self.match.object, noMatch=43)
        self.match.expect(42).andReturn(44)
        self.expectSuccess([42], 44)
        self.expectSuccess([], 43)

    def testRepetition(self):
        self.p = RepetitionParser(LiteralParser(42), match=self.match.object)
        self.match.expect([42, 42]).andReturn(43)
        self.expectSuccess([42, 42], 43)
