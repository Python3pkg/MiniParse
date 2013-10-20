#!/usr/bin/env python

import unittest


# EBNF Grammar

# stringExpr = stringTerm, { '+', stringTerm };
# stringTerm = [ ( intTerm | '(', intExpr, ')' ), '*' ], string;
# intExpr = intTerm, { ( '+' | '-' ) , intTerm };
# intTerm = { intFactor, ( '*' | '/' ) }, intFactor;
# intFactor = int | '(', intExpr, ')';
# int = [ '-' ], digit, { digit };
# digit = '0' | '1' | '...' | '9';
# string = '"', { stringElement }, '"';
# stringElement = char | escape;
# escape = '\"' | '\\';

# Abstract syntax tree classes


def containerOfMany(name):
    class C:
        def __init__(self, contents):
            self.__contents = contents

        def dump(self):
            if len(self.__contents) == 1:
                return self.__contents[0].dump()
            else:
                return name + "(" + ", ".join(c.dump() for c in self.__contents) + ")"

    C.__name__ = name
    return C


StringExpr = containerOfMany("StringExpr")
String = containerOfMany("String")


class Char:
    def __init__(self, value):
        self.value = value

    def dump(self):
        return "'" + self.value + "'"


class Escape:
    def __init__(self, value):
        self.value = value

    def dump(self):
        return "<" + self.value + ">"


# Parser


class ParsingError(Exception):
    pass


class Cursor(object):
    def __init__(self, s):
        self.__s = s
        self.__i = 0

    def get(self, n):
        self.__assertNMoreChars(n)
        return self.__get(n)

    def __assertNMoreChars(self, n):
        assert self.__i + n <= len(self.__s)

    def __get(self, n):
        return self.__s[self.__i:self.__i + n]

    def advance(self, n):
        v = self.get(n)
        self.__i += n
        return v

    def startswith(self, s):
        return self.__get(len(s)) == s

    def consume(self, s):
        assert self.startswith(s)
        self.advance(len(s))

    @property
    def finished(self):
        return self.__i == len(self.__s)

    @property
    def position(self):
        return self.__i

    def consumeSpaces(self):
        while self.__get(1) in (" ", "\t"):
            self.advance(1)


class CursorTestCase(unittest.TestCase):
    def setUp(self):
        self.c = Cursor("abcde")

    def testAdvanceToEnd(self):
        self.assertEqual(self.c.advance(4), "abcd")
        self.assertFalse(self.c.finished)
        self.assertEqual(self.c.advance(1), "e")
        self.assertTrue(self.c.finished)

    def testConsumeToEnd(self):
        self.c.consume("abcd")
        self.assertFalse(self.c.finished)
        self.assertEqual(self.c.position, 4)
        self.assertEqual(self.c.get(1), "e")
        self.c.consume("e")
        self.assertTrue(self.c.finished)


def parse(s):
    c = Cursor(s)
    return expect(parseStringExpr, c)


def expect(parse, c):
    ok, exprOrError = parse(c)
    if ok:
        return exprOrError
    else:
        raise ParsingError(c.position, exprOrError)


def expectChar(e, c):
    if c.startswith(e):
        c.consume(e)
    else:
        raise ParsingError(c.position, "Expected '" + e + "'")


def parseStringExpr(c):
    terms = [expect(parseStringTerm, c)]
    while not c.finished:
        c.consumeSpaces()
        expectChar("+", c)
        c.consumeSpaces()
        terms.append(expect(parseStringTerm, c))
    return True, StringExpr(terms)


def parseStringTerm(c):
    return parseString(c)


def parseString(c):
    # if c.startswith('"'):
        c.consume('"')
        elements = []
        while not c.startswith('"'):
            if c.finished:
                return False, "Hit EOF while parsing string"
            elements.append(expect(parseStringElement, c))
        c.consume('"')
        return True, String(elements)
    # else:
        # return False, "Expected '\"'"


def parseStringElement(c):
    if c.startswith("\\"):
        c.consume("\\")
        if c.get(1) in ('"', '\\'):
            return True, Escape(c.advance(1))
        return False, "Expected '\"' or '\\'"
    # elif c.startswith('"'):
    #     return False, "Unexpected '\"'"
    else:
        return True, Char(c.advance(1))


class TestCase(unittest.TestCase):
    def parseDump(self, input, expectedOutput):
        actualOutput = parse(input).dump()
        self.assertEqual(actualOutput, expectedOutput)

    def expectParsingError(self, input, expectedPosition, expectedMessage):
        with self.assertRaises(ParsingError) as cm:
            actualOutput = parse(input).dump()
        exception = cm.exception
        actualPosition, actualMessage = exception.args
        self.assertIsInstance(exception, ParsingError)
        self.assertEqual(actualPosition, expectedPosition)
        self.assertEqual(actualMessage, expectedMessage)

    def testSimpleString(self):
        self.parseDump('"abc"', "String('a', 'b', 'c')")

    def testStringWithEscapes(self):
        self.parseDump('"a\\"b\\\\c"', "String('a', <\">, 'b', <\\>, 'c')")

    def testUnterminatedString(self):
        self.expectParsingError('"abc', 4, "Hit EOF while parsing string")

    def testTrailingJunk(self):
        self.expectParsingError('"abc"xxx', 5, "Expected '+'")

    def testBadEscapeSequence(self):
        self.expectParsingError('"ab\\c"', 4, "Expected '\"' or '\\'")

    def testStringAddition(self):
        self.parseDump('"abc" + "def"', "StringExpr(String('a', 'b', 'c'), String('d', 'e', 'f'))")


if __name__ == "__main__":  # pragma no branch
    unittest.main()
