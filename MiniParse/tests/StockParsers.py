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
from MiniParse import LiteralParser


class LiteralParserTestCase(unittest.TestCase):
    def setUp(self):
        self.p = LiteralParser(42)

    def testSuccess(self):
        self.assertEqual(parse(self.p, [42]), 42)

    def testFailure(self):
        with self.assertRaises(SyntaxError) as cm:
            parse(self.p, [41])
        self.assertEqual(cm.exception.position, 0)
        self.assertEqual(cm.exception.expected, set([42]))

    def testPartialSuccess(self):
        with self.assertRaises(SyntaxError) as cm:
            parse(self.p, [42, 43])
        self.assertEqual(cm.exception.position, 1)
        self.assertEqual(cm.exception.expected, set())
