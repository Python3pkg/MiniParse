# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest

import MiniParse
import Parser


class StringArithmeticTestCase(unittest.TestCase):
    def parseAndDump(self, input, expectedOutput):
        actualOutput = Parser.Parser()(input).dump()
        self.assertEqual(actualOutput, expectedOutput)

    def expectParsingError(self, input, expectedPosition, expectedExpected):
        with self.assertRaises(MiniParse.ParsingError) as cm:
            actualOutput = Parser.Parser()(input)
        self.assertEqual(cm.exception.message, "Syntax error")
        self.assertEqual(cm.exception.position, expectedPosition)
        self.assertEqual(cm.exception.expected, set(expectedExpected))

    def testSimpleString(self):
        self.parseAndDump('"abcdef"', "abcdef")

    def testEmptyInput(self):
        self.expectParsingError('', 0, ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", '"', "(", "-"])

    def testForbidenChar(self):
        self.expectParsingError('"A"', 1, ["a", "b", "c", "d", "e", "f", '"'])

    def testUnterminatedString(self):
        self.expectParsingError('"abc', 4, ["a", "b", "c", "d", "e", "f", '"'])

    def testTrailingJunk(self):
        self.expectParsingError('"abc"xxx', 5, ["+"])

    def testStringAddition(self):
        self.parseAndDump('"abc"+"def"', "abcdef")

    def testStringMultiplication(self):
        self.parseAndDump('2*"abc"', "abcabc")
        self.parseAndDump('2*2*"abc"', "abcabcabcabc")
        self.parseAndDump('2*2*2*"abc"', "abcabcabcabcabcabcabcabc")
        self.parseAndDump('10*"a"', "aaaaaaaaaa")

    def testIntAddition(self):
        self.parseAndDump('(1)*"abc"', "abc")
        self.parseAndDump('(1+1)*"abc"', "abcabc")
        self.parseAndDump('(1+1+1)*"abc"', "abcabcabc")

    def testBadAddition_1(self):
        self.expectParsingError('(1+a)*"abc"', 3, ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "(", "-"])

    def testBadAddition_2(self):
        self.expectParsingError('(a+1)*"abc"', 1, ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "(", "-", '"'])

    def testBadStringFactor(self):
        self.expectParsingError('(1+1)*a', 6, ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "(", "-", '"'])

    def testNegativeNumbers(self):
        self.parseAndDump('(2+-1)*"abc"', "abc")

    def testDivision(self):
        self.parseAndDump('(8/4)*"abc"', "abcabc")

    def testSubstraction(self):
        self.parseAndDump('(8-6)*"abc"', "abcabc")

    def testStringExpr(self):
        self.parseAndDump('("abc")', "abc")
        self.parseAndDump('(1+1)*("abc"+"def")', "abcdefabcdef")

    def testBadOperation(self):
        self.expectParsingError('(1%1)*"a"', 2, ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-", "+", "*", "/", ")"])
