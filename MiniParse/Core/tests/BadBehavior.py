# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest
import MockMockMock

from MiniParse import parse
from MiniParse import SequenceParser
from MiniParse.Core.Cursor import Cursor


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
