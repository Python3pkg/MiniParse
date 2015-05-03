# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest
import MockMockMock

from MiniParse import LiteralParser, SequenceParser, AlternativeParser, OptionalParser, RepeatedParser
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
        self.match.expect(42, 43).andReturn(45)
        self.expectSuccess([42, 43], 45)

    def testOptionalParser(self):
        self.p = OptionalParser(LiteralParser(42), match=self.match.object, noMatch=43)
        self.match.expect(42).andReturn(44)
        self.expectSuccess([42], 44)
        self.expectSuccess([], 43)

    def testRepetition(self):
        self.p = RepeatedParser(LiteralParser(42), match=self.match.object)
        self.match.expect([42, 42]).andReturn(43)
        self.expectSuccess([42, 42], 43)
