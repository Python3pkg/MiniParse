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
from MiniParse import SequenceParser
from MiniParse.Cursor import Cursor


class TestCase(unittest.TestCase):
    def testExceptionsRaisedByParsersAreNotModified(self):
        mocks = MockMockMock.Engine()
        parser = mocks.create("parser")
        e = Exception()
        parser.expect.apply.withArguments(lambda args, kwds: True).andRaise(e)
        with self.assertRaises(Exception) as cm:
            parse(SequenceParser([parser.object]), "")
        self.assertIs(cm.exception, e)

    def testNotEndingTheBacktrackingRaisesAssertionError(self):
        cursor = Cursor("")
        with self.assertRaises(AssertionError):
            with cursor.backtracking as bt:
                cursor.success(42)  # should have been bt.success(42)
