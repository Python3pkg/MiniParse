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

class String:
    def __init__(self, elements):
        self.elements = elements

    def dump(self):
        return "String(" + ", ".join(e.dump() for e in self.elements) + ")"


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


def parse(s):
    ok, remaining, exprOrError = parseStringExpr(s)
    if ok:
        assert remaining == "", remaining
        return exprOrError
    else:
        raise ParsingError(s[:len(s) - len(remaining)], remaining, exprOrError)

def parseStringExpr(s):
    return parseString(s)

def parseString(s):
    if s.startswith('"'):
        s = s[1:]
        elements = []
        while not s.startswith('"'):
            ok, s, element = acceptStringElement(s)
            if not ok:
                return False, s, element
            elements.append(element)
        assert s.startswith('"')
        s = s[1:]
        return True, s, String(elements)

def acceptStringElement(s):
    if s.startswith("\\"):
        s = s[1:]
        if s[0] in ('"', '\\'):
            return True, s[1:], Escape(s[0])
        return False, s, "Expected '\"' or '\\'"
    if len(s) == 0:
        return False, s, "Hit EOF while parsing string"
    else:
        assert s[0] != '"'
        return True, s[1:], Char(s[0])


class TestCase(unittest.TestCase):
    def parseDump(self, i, o):
        self.assertEqual(parse(i).dump(), o)

    def expectParsingError(self, i, o, m):
        with self.assertRaises(ParsingError) as cm:
            parse(i)
        a, b, message = cm.exception.args
        self.assertEqual(a + b, i)
        self.assertEqual(a, o)
        self.assertEqual(message, m)

    def testSimpleString(self):
        self.parseDump('"abc"', "String('a', 'b', 'c')")

    def testStringWithEscapes(self):
        self.parseDump('"a\\"b\\\\c"', "String('a', <\">, 'b', <\\>, 'c')")

    def testUnterminatedString(self):
        self.expectParsingError('"abc', '"abc', "Hit EOF while parsing string")

    def testBadEscapeSequence(self):
        self.expectParsingError('"ab\\c"', '"ab\\', "Expected '\"' or '\\'")


if __name__ == "__main__":
    unittest.main()
