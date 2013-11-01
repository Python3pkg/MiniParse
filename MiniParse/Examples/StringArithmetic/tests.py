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

import MiniParse
import Parser


class StringArithmeticTestCase(unittest.TestCase):
    def parseAndDump(self, input, expectedOutput):
        actualOutput = Parser.Parser()(input).dump()
        self.assertEqual(actualOutput, expectedOutput)

    def expectSyntaxError(self, input, expectedPosition, expectedExpected):
        with self.assertRaises(MiniParse.SyntaxError) as cm:
            actualOutput = Parser.Parser()(input)
        exception = cm.exception
        actualPosition, actualExpected = exception.args
        self.assertEqual(actualPosition, expectedPosition)
        self.assertEqual(actualExpected, set(expectedExpected))

    def testSimpleString(self):
        self.parseAndDump('"abcdef"', "abcdef")

    def testEmptyInput(self):
        self.expectSyntaxError('', 0, ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", '"', "(", "-"])

    def testForbidenChar(self):
        self.expectSyntaxError('"A"', 1, ["a", "b", "c", "d", "e", "f", '"'])

    def testUnterminatedString(self):
        self.expectSyntaxError('"abc', 4, ["a", "b", "c", "d", "e", "f", '"'])

    def testTrailingJunk(self):
        self.expectSyntaxError('"abc"xxx', 5, ["+"])

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
        self.expectSyntaxError('(1+a)*"abc"', 3, ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "(", "-"])

    def testBadAddition_2(self):
        self.expectSyntaxError('(a+1)*"abc"', 1, ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "(", "-", '"'])

    def testBadStringFactor(self):
        self.expectSyntaxError('(1+1)*a', 6, ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "(", "-", '"'])

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
        self.expectSyntaxError('(1%1)*"a"', 2, ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-", "+", "*", "/", ")"])
