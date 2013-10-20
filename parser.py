#!/usr/bin/env python

import unittest


# Abstract syntax tree classes


class StringExpr:
    def __init__(self, terms):
        self.__terms = terms

    def dump(self):
        return "".join(t.dump() for t in self.__terms)


class String:
    def __init__(self, elements):
        self.__elements = elements

    def dump(self):
        return "".join(e.dump() for e in self.__elements)


class Char:
    def __init__(self, value):
        self.__value = value

    def dump(self):
        return self.__value


class Escape:
    def __init__(self, value):
        self.__value = value

    def dump(self):
        return self.__value


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

    @property
    def finished(self):
        return self.__i == len(self.__s)

    @property
    def position(self):
        return self.__i

    def discardSpaces(self):
        while self.__get(1) in (" ", "\t"):
            self.advance(1)


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
        c.advance(len(e))
    else:
        raise ParsingError(c.position, "Expected '" + e + "'")


# Grammar rule: stringExpr = stringTerm, { '+', stringTerm };
def parseStringExpr(c):
    terms = [expect(parseStringTerm, c)]
    while not c.finished:
        c.discardSpaces()
        expectChar("+", c)
        c.discardSpaces()
        terms.append(expect(parseStringTerm, c))
    return True, StringExpr(terms)


# Grammar rule: stringTerm = [ intTerm, '*' ], stringFactor;
def parseStringTerm(c):
    return parseString(c)


# Grammar rule: stringFactor = ( string | '(', stringExpr, ')' );
# Grammar rule: intTerm = intFactor, { ( '*' | '/' ), intFactor };
# Grammar rule: intFactor = int | '(', intExpr, ')';
# Grammar rule: intExpr = intTerm, { ( '+' | '-' ) , intTerm };
# Grammar rule: int = [ '-' ], digit, { digit };
# Grammar rule: digit = '0' | '1' | '...' | '9';


# Grammar rule: string = '"', { stringElement }, '"';
def parseString(c):
    # if c.startswith('"'):
        expectChar('"', c)
        elements = []
        while not c.startswith('"'):
            if c.finished:
                return False, "Hit EOF while parsing string"
            elements.append(expect(parseStringElement, c))
        expectChar('"', c)
        return True, String(elements)
    # else:
        # return False, "Expected '\"'"


# Grammar rule: stringElement = char | escape;
# Grammar rule: escape = '\"' | '\\';
def parseStringElement(c):
    if c.startswith("\\"):
        expectChar('\\', c)
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
        self.parseDump('"abc"', "abc")

    def testStringWithEscapes(self):
        self.parseDump('"a\\"b\\\\c"', "a\"b\\c")

    def testUnterminatedString(self):
        self.expectParsingError('"abc', 4, "Hit EOF while parsing string")

    def testTrailingJunk(self):
        self.expectParsingError('"abc"xxx', 5, "Expected '+'")

    def testBadEscapeSequence(self):
        self.expectParsingError('"ab\\c"', 4, "Expected '\"' or '\\'")

    def testStringAddition(self):
        self.parseDump('"abc" + "def"', "abcdef")


if __name__ == "__main__":  # pragma no branch
    unittest.main()
