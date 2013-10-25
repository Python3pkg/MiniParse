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

# Rewrite: should not change
from MiniParse import OptionalParser, SequenceParser, AlternativeParser, LiteralParser, RepeatedParser, SyntaxError
# Rewrite: will change
from MiniParse import ParsingSuccess, Cursor


# Rewrite: implementation will change
def parse(s):
    c = Cursor(s)
    r = StringExpr.parse(c)
    if not r.ok:
        raise SyntaxError(r.position, "Expected " + " or ".join(sorted(r.expected)))
    elif not c.finished:
        raise SyntaxError(r.failure.position, "Expected " + " or ".join(sorted(r.failure.expected)))
    else:
        return r.value


# Grammar rule: stringExpr = stringTerm, { '+', stringTerm };
class StringExpr:
    def __init__(self, terms):
        assert all(isinstance(term, StringTerm) for term in terms)
        self.__terms = terms

    def dump(self):
        return "".join(t.dump() for t in self.__terms)

    @staticmethod
    def parse(c):
        r = SequenceParser(
            [
                StringTerm,
                RepeatedParser(
                    SequenceParser(
                        [
                            LiteralParser("+"),
                            StringTerm
                        ]
                    )
                )
            ]
        ).parse(c)
        if r.ok:
            terms = [r.value[0]]
            terms += [v[1] for v in r.value[1]]
            return ParsingSuccess(StringExpr(terms), r.failure)
        else:
            return r


# Grammar rule: stringTerm = [ intTerm, '*' ], stringFactor;
class StringTerm:
    def __init__(self, i, s):
        assert i is None or isinstance(i, IntTerm)
        assert isinstance(s, StringFactor)
        self.__i = i
        self.__s = s

    def dump(self):
        s = self.__s.dump()
        if self.__i is None:
            i = 1
        else:
            i = self.__i.compute()
        return i * s

    @staticmethod
    def parse(c):
        r = SequenceParser(
            [
                OptionalParser(
                    SequenceParser(
                        [
                            IntTerm,
                            LiteralParser("*")
                        ]
                    )
                ),
                StringFactor
            ]
        ).parse(c)
        if r.ok:
            i = r.value[0]
            if i is not None:
                i = i[0]
            s = r.value[1]
            return ParsingSuccess(StringTerm(i, s), r.failure)
        else:
            return r


# Grammar rule: stringFactor = string | '(', stringExpr, ')';
class StringFactor:
    def __init__(self, real):
        assert isinstance(real, (String, StringExpr))
        self.__real = real

    def dump(self):
        return self.__real.dump()

    @staticmethod
    def parse(c):
        r = AlternativeParser(
            [
                String,
                SequenceParser(
                    [
                        LiteralParser("("),
                        StringExpr,
                        LiteralParser(")")
                    ]
                )
            ]
        ).parse(c)
        if r.ok:
            if isinstance(r.value, String):
                return ParsingSuccess(StringFactor(r.value), r.failure)
            else:
                return ParsingSuccess(StringFactor(r.value[1]), r.failure)
        else:
            return r


# Grammar rule: intTerm = intFactor, { ( '*' | '/' ), intFactor };
class IntTerm:
    def __init__(self, factors):
        assert all(factor[0] in ("*", "/") for factor in factors)
        assert all(isinstance(factor[1], IntFactor) for factor in factors)
        self.__factors = factors

    def compute(self):
        v = 1
        for mult, f in self.__factors:
            if mult == "*":
                v *= f.compute()
            else:
                v //= f.compute()
        return v

    @staticmethod
    def parse(c):
        r = SequenceParser(
            [
                IntFactor,
                RepeatedParser(
                    SequenceParser(
                        [
                            AlternativeParser([LiteralParser("*"), LiteralParser("/")]),
                            IntFactor
                        ]
                    )
                )
            ]
        ).parse(c)
        if r.ok:
            factors = [("*", r.value[0])]
            factors += r.value[1]
            return ParsingSuccess(IntTerm(factors), r.failure)
        else:
            return r


# Grammar rule: intFactor = int | '(', intExpr, ')';
class IntFactor:
    def __init__(self, real):
        assert isinstance(real, (Int, IntExpr))
        self.__real = real

    def compute(self):
        return self.__real.compute()

    @staticmethod
    def parse(c):
        r = AlternativeParser(
            [
                Int,
                SequenceParser(
                    [
                        LiteralParser("("),
                        IntExpr,
                        LiteralParser(")")
                    ]
                )
            ]
        ).parse(c)
        if r.ok:
            if isinstance(r.value, Int):
                return ParsingSuccess(IntFactor(r.value), r.failure)
            else:
                return ParsingSuccess(IntFactor(r.value[1]), r.failure)
        else:
            return r


# Grammar rule: intExpr = intTerm, { ( '+' | '-' ) , intTerm };
class IntExpr:
    def __init__(self, terms):
        assert all(term[0] in ("+", "-") for term in terms)
        assert all(isinstance(term[1], IntTerm) for term in terms)
        self.__terms = terms

    def compute(self):
        v = 0
        for add, term in self.__terms:
            if add == "+":
                v += term.compute()
            else:
                v -= term.compute()
        return v

    @staticmethod
    def parse(c):
        r = SequenceParser(
            [
                IntTerm,
                RepeatedParser(
                    SequenceParser(
                        [
                            AlternativeParser([LiteralParser("+"), LiteralParser("-")]),
                            IntTerm
                        ]
                    )
                )
            ]
        ).parse(c)
        if r.ok:
            terms = [("+", r.value[0])]
            terms += r.value[1]
            return ParsingSuccess(IntExpr(terms), r.failure)
        else:
            return r


# Grammar rule: int = [ '-' ], digit, { digit };
class Int:
    def __init__(self, negativeSign, digits):
        assert negativeSign is None or negativeSign is "-"
        assert all(isinstance(digit, Digit) for digit in digits)
        self.__negativeSign = negativeSign
        self.__digits = digits

    def compute(self):
        v = int("".join(d.value for d in self.__digits))
        if self.__negativeSign:
            return -v
        else:
            return v

    @staticmethod
    def parse(c):
        r = SequenceParser(
            [
                OptionalParser(LiteralParser("-")),
                Digit,
                RepeatedParser(Digit)
            ]
        ).parse(c)
        if r.ok:
            digits = [r.value[1]]
            digits += r.value[2]
            return ParsingSuccess(Int(r.value[0], digits), r.failure)
        else:
            return r


# Grammar rule: digit = '0' | '1' | '...' | '9';
class Digit:
    def __init__(self, value):
        assert isinstance(value, str)
        self.value = value

    @staticmethod
    def parse(c):
        r = AlternativeParser(
            [
                LiteralParser("0"),
                LiteralParser("1"),
                LiteralParser("2"),
                LiteralParser("3"),
                LiteralParser("4"),
                LiteralParser("5"),
                LiteralParser("6"),
                LiteralParser("7"),
                LiteralParser("8"),
                LiteralParser("9")
            ],
            expected="0-9"
        ).parse(c)
        if r.ok:
            return ParsingSuccess(Digit(r.value), r.failure)
        else:
            return r


# Grammar rule: string = '"', { stringElement }, '"';
class String:
    def __init__(self, elements):
        assert all(isinstance(element, StringElement) for element in elements)
        self.__elements = elements

    def dump(self):
        return "".join(e.dump() for e in self.__elements)

    @staticmethod
    def parse(c):
        r = SequenceParser(
            [
                LiteralParser('"', expected="opening quote"),
                RepeatedParser(StringElement),
                LiteralParser('"', expected="closing quote")
            ]
        ).parse(c)
        if r.ok:
            return ParsingSuccess(String(r.value[1]), r.failure)
        else:
            return r


# Grammar rule: stringElement = char | escape;
class StringElement:
    def __init__(self, real):
        assert isinstance(real, (Char, Escape))
        self.__real = real

    def dump(self):
        return self.__real.dump()

    @staticmethod
    def parse(c):
        r = AlternativeParser([Char, Escape]).parse(c)
        if r.ok:
            return ParsingSuccess(StringElement(r.value), r.failure)
        else:
            return r


# Grammar rule: char = 'a' | 'b' | '...' | 'z';
class Char:
    def __init__(self, value):
        assert isinstance(value, str)
        self.__value = value

    def dump(self):
        return self.__value

    @staticmethod
    def parse(c):
        r = AlternativeParser(
            [
                LiteralParser("a"),
                LiteralParser("b"),
                LiteralParser("c"),
                LiteralParser("d"),
                LiteralParser("e"),
                LiteralParser("f"),
                LiteralParser("g"),
                LiteralParser("h"),
                LiteralParser("i"),
                LiteralParser("j"),
                LiteralParser("k"),
                LiteralParser("l"),
                LiteralParser("m"),
                LiteralParser("n"),
                LiteralParser("o"),
                LiteralParser("p"),
                LiteralParser("q"),
                LiteralParser("r"),
                LiteralParser("s"),
                LiteralParser("t"),
                LiteralParser("u"),
                LiteralParser("v"),
                LiteralParser("w"),
                LiteralParser("x"),
                LiteralParser("y"),
                LiteralParser("z")
            ],
            expected="a-z"
        ).parse(c)
        if r.ok:
            return ParsingSuccess(Char(r.value), r.failure)
        else:
            return r


# Grammar rule: escape = '\"' | '\\';
class Escape:
    def __init__(self, value):
        assert isinstance(value, str)
        self.__value = value

    def dump(self):
        return self.__value

    @staticmethod
    def parse(c):
        r = SequenceParser(
            [
                LiteralParser("\\"),
                AlternativeParser([LiteralParser("\\"), LiteralParser("\"")])
            ],
            expected="escape sequence"
        ).parse(c)
        if r.ok:
            return ParsingSuccess(Escape(r.value[1]), r.failure)
        else:
            return r


# Rewrite: tests shouldn't change
class TestCase(unittest.TestCase):
    def parseAndDump(self, input, expectedOutput):
        actualOutput = parse(input).dump()
        self.assertEqual(actualOutput, expectedOutput)

    def expectSyntaxError(self, input, expectedPosition, expectedMessage):
        with self.assertRaises(SyntaxError) as cm:
            actualOutput = parse(input).dump()
        exception = cm.exception
        actualPosition, actualMessage = exception.args
        self.assertIsInstance(exception, SyntaxError)
        self.assertEqual((actualPosition, actualMessage), (expectedPosition, expectedMessage))

    def testSimpleString(self):
        self.parseAndDump('"abc"', "abc")
        self.parseAndDump('"abcdefghijklmnopqrstuvwxyz"', "abcdefghijklmnopqrstuvwxyz")

    def testEmptyInput(self):
        self.expectSyntaxError('', 0, "Expected '(' or '-' or 0-9 or opening quote")

    def testForbidenChar(self):
        self.expectSyntaxError('"A"', 1, "Expected a-z or closing quote or escape sequence")

    def testStringWithEscapes(self):
        self.parseAndDump('"a\\"b\\\\c"', "a\"b\\c")

    def testUnterminatedString(self):
        self.expectSyntaxError('"abc', 4, "Expected a-z or closing quote or escape sequence")

    def testTrailingJunk(self):
        self.expectSyntaxError('"abc"xxx', 5, "Expected '+'")

    def testBadEscapeSequence(self):
        self.expectSyntaxError('"ab\\c"', 4, "Expected escape sequence")

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
        self.expectSyntaxError('(1+a)*"abc"', 3, "Expected '(' or '-' or 0-9")

    def testBadAddition_2(self):
        self.expectSyntaxError('(a+1)*"abc"', 1, "Expected '(' or '-' or 0-9 or opening quote")

    def testBadStringFactor(self):
        self.expectSyntaxError('(1+1)*a', 6, "Expected '(' or '-' or 0-9 or opening quote")

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
        self.expectSyntaxError('(1%1)*"a"', 2, "Expected ')' or '*' or '+' or '-' or '/' or 0-9")
