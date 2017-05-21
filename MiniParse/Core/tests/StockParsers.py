# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest

from MiniParse import LiteralParser, SequenceParser, AlternativeParser, OptionalParser, RepeatedParser
from .Framework import ParserTestCase


class LiteralTestCase(ParserTestCase):
    def setUp(self):
        self.p = LiteralParser(42)

    def testSuccess(self):
        self.expectSuccess([42], 42)

    def testFailure1(self):
        self.expectFailure([41], 0, [42])

    def testFailure10(self):
        self.expectFailure([], 0, [42])

    def testPartialSuccess(self):
        self.expectFailure([42, 43], 1, [])


class SequenceTestCase(ParserTestCase):
    def setUp(self):
        self.p = SequenceParser([
            LiteralParser(42),
            LiteralParser(43),
            LiteralParser(44),
            LiteralParser(45)
        ])

    def testSuccess(self):
        self.expectSuccess([42, 43, 44, 45], (42, 43, 44, 45))

    def testFailure0(self):
        self.expectFailure([], 0, [42])

    def testFailure1(self):
        self.expectFailure([41], 0, [42])

    def testFailure10(self):
        self.expectFailure([42], 1, [43])

    def testFailure2(self):
        self.expectFailure([42, 41], 1, [43])

    def testFailure20(self):
        self.expectFailure([42, 43], 2, [44])

    def testFailure3(self):
        self.expectFailure([42, 43, 41], 2, [44])

    def testFailure30(self):
        self.expectFailure([42, 43, 44], 3, [45])

    def testFailure4(self):
        self.expectFailure([42, 43, 44, 41], 3, [45])

    def testPartialSuccess(self):
        self.expectFailure([42, 43, 44, 45, 46], 4, [])


class UnambiguousAlternativeTestCase(ParserTestCase):
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

    def testFailure00(self):
        self.expectFailure([], 0, [42, 44, 46])

    def testFailure1(self):
        self.expectFailure([42, 41], 1, [43])

    def testFailure10(self):
        self.expectFailure([42], 1, [43])

    def testFailure2(self):
        self.expectFailure([44, 41], 1, [45])

    def testFailure20(self):
        self.expectFailure([44], 1, [45])

    def testFailure3(self):
        self.expectFailure([46, 41], 1, [47])

    def testFailure30(self):
        self.expectFailure([46], 1, [47])

    def testPartialSuccess1(self):
        self.expectFailure([42, 43, 41], 2, [])

    def testPartialSuccess2(self):
        self.expectFailure([44, 45, 41], 2, [])

    def testPartialSuccess3(self):
        self.expectFailure([46, 47, 41], 2, [])


class AlternativeWithCommonPrefixAndDifferentLengthsTestCase(ParserTestCase):
    def setUp(self):
        self.p = AlternativeParser([
            SequenceParser([LiteralParser(42), LiteralParser(43)]),
            SequenceParser([LiteralParser(42), LiteralParser(44), LiteralParser(45)]),
            LiteralParser(42)
        ])

    def testSuccess1(self):
        self.expectSuccess([42, 43], (42, 43))

    def testSuccess2(self):
        self.expectSuccess([42, 44, 45], (42, 44, 45))

    def testSuccess3(self):
        self.expectSuccess([42], 42)

    def testFailure1(self):
        self.expectFailure([], 0, [42])

    def testFailure2(self):
        self.expectFailure([41], 0, [42])

    def testFailure3(self):
        self.expectFailure([42, 41], 1, [43, 44])

    def testFailure4(self):
        self.expectFailure([42, 43, 41], 2, [])

    def testFailure5(self):
        self.expectFailure([42, 44, 45, 41], 3, [])

    def testFailure6(self):
        self.expectFailure([42, 44, 41], 2, [45])


class OptionalTestCase(ParserTestCase):
    def setUp(self):
        self.p = OptionalParser(LiteralParser(42))

    def testSuccess1(self):
        self.expectSuccess([], None)

    def testSuccess2(self):
        self.expectSuccess([42], 42)

    def testFailure1(self):
        self.expectFailure([41], 0, [42])

    def testFailure2(self):
        self.expectFailure([42, 41], 1, [])


class RepetitionTestCase(ParserTestCase):
    def setUp(self):
        self.p = RepeatedParser(LiteralParser(42))

    def testSuccess0(self):
        self.expectSuccess([], [])

    def testSuccess1(self):
        self.expectSuccess([42, 42, 42], [42, 42, 42])

    def testFailure1(self):
        self.expectFailure([42, 42, 41], 2, [42])
