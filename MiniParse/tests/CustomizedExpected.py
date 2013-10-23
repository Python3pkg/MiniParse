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
    def expect(self, expected):
        self.expectFailure("", 0, [expected])

    def testLiteralParser(self):
        self.p = LiteralParser(42, "expected")
        self.expect("expected")

    def testAlternativeParser(self):
        self.p = AlternativeParser([LiteralParser(42), LiteralParser(43)], "expected")
        self.expect("expected")

    def testSequenceParser(self):
        self.p = SequenceParser([LiteralParser(42), LiteralParser(43)], "expected")
        self.expect("expected")
