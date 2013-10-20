#!/usr/bin/env python

import unittest


class SyntaxError(Exception):
    pass


class Cursor(object):
    def __init__(self, s):
        self.__s = s
        self.__i = 0

    def get(self, n):
        assert self.__i + n <= len(self.__s)
        return self.__get(n)

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

    def reset(self, i):
        self.__i = i


class ParsingFailure:
    def __init__(self, reason):
        self.ok = False
        self.reason = reason


class ParsingSuccess:
    def __init__(self, value):
        self.ok = True
        self.value = value


def parse(s):
    c = Cursor(s)
    r = parseStringExpr(c)
    if not r.ok:
        raise SyntaxError(c.position, r.reason)
    elif not c.finished:
        raise SyntaxError(c.position, "WTF")
    else:
        return r.value


# Grammar rule: stringExpr = stringTerm, { '+', stringTerm };
class StringExpr:
    def __init__(self, terms):
        self.__terms = terms

    def dump(self):
        return "".join(t.dump() for t in self.__terms)


def parseStringExpr(c):
    terms = []
    termParsingResult = parseStringTerm(c)
    while termParsingResult.ok:
        terms.append(termParsingResult.value)
        if c.finished:
            return ParsingSuccess(StringExpr(terms))
        else:
            if c.startswith("+"):
                c.advance(1)
                termParsingResult = parseStringTerm(c)
            else:
                return ParsingFailure("Expected '+'")
    return termParsingResult


# Grammar rule: stringTerm = [ intTerm, '*' ], stringFactor;
class StringTerm:
    def __init__(self, i, s):
        self.__i = i
        self.__s = s

    def dump(self):
        s = self.__s.dump()
        i = self.__i.compute()
        return i * s


def parseStringTerm(c):
    rInt = IntTerm.parse(c)
    if rInt.ok:
        if c.startswith("*"):
            c.advance(1)
            rString = parseStringFactor(c)
            if rString.ok:
                return ParsingSuccess(StringTerm(rInt.value, rString.value))
            else:
                return rString
        else:
            return ParsingFailure("Expected '*' (then stringFactor)")
    else:
        return parseStringFactor(c)


# Grammar rule: stringFactor = ( string | '(', stringExpr, ')' );
def parseStringFactor(c):
    return parseString(c)


# Grammar rule: intTerm = intFactor, { ( '*' | '/' ), intFactor };
class IntTerm:
    def __init__(self, factors):
        self.__factors = factors

    def compute(self):
        v = 1
        for f in self.__factors:
            v *= f.compute()
        return v

    @staticmethod
    def parse(c):
        factors = []
        r = parseIntFactor(c)
        while r.ok:
            factors.append(r.value)
            r = IntTerm.__parseTimesIntFactor(c)
        if len(factors) == 0:
            return ParsingFailure("Expected intTerm")
        else:
            return ParsingSuccess(IntTerm(factors))

    @staticmethod
    def __parseTimesIntFactor(c):
        origPos = c.position
        if c.startswith("*"):
            c.advance(1)
            r = parseIntFactor(c)
            if r.ok:
                return r
            else:
                c.reset(origPos)
                return r
        else:
            return ParsingFailure("Expected '*'")


# Grammar rule: intFactor = int | '(', intExpr, ')';
def parseIntFactor(c):
    return parseInt(c)


# Grammar rule: intExpr = intTerm, { ( '+' | '-' ) , intTerm };


# Grammar rule: int = [ '-' ], digit, { digit };
# Grammar rule: digit = '0' | '1' | '...' | '9';
class Int:
    def __init__(self, value):
        self.__value = value

    def compute(self):
        return self.__value


def parseInt(c):
    digits = ""
    while c.get(1) in "0123456789":
        digits += c.advance(1)
    if len(digits) == 0:
        return ParsingFailure("Expected a digit")
    else:
        return ParsingSuccess(Int(int(digits)))


# Grammar rule: string = '"', { stringElement }, '"';
class String:
    def __init__(self, elements):
        self.__elements = elements

    def dump(self):
        return "".join(e.dump() for e in self.__elements)


def parseString(c):
    if c.startswith('"'):
        c.advance(1)
        elements = []
        r = parseStringElement(c)
        while r.ok:
            elements.append(r.value)
            r = parseStringElement(c)
        if r.reason != "Normal string end":
            return r
        if c.startswith('"'):
            c.advance(1)
            return ParsingSuccess(String(elements))
        else:
            return ParsingFailure("Expected closing quote '\"'")
    else:
        return ParsingFailure("Expected opening quote '\"'")


# Grammar rule: stringElement = char | escape;
# Grammar rule: escape = '\"' | '\\';
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


def parseStringElement(c):
    if c.startswith("\\"):
        if c.get(2) in ('\\"', '\\\\'):
            c.advance(1)
            return ParsingSuccess(Escape(c.advance(1)))
        else:
            return ParsingFailure("Bad escape sequence")
    elif c.startswith('"'):
        return ParsingFailure("Normal string end")
    elif c.finished:
        return ParsingFailure("Unexpected end of file")
    else:
        return ParsingSuccess(Char(c.advance(1)))


class TestCase(unittest.TestCase):
    def parseDump(self, input, expectedOutput):
        actualOutput = parse(input).dump()
        self.assertEqual(actualOutput, expectedOutput)

    def expectSyntaxError(self, input, expectedPosition, expectedMessage):
        with self.assertRaises(SyntaxError) as cm:
            actualOutput = parse(input).dump()
        exception = cm.exception
        actualPosition, actualMessage = exception.args
        self.assertIsInstance(exception, SyntaxError)
        self.assertEqual(actualPosition, expectedPosition)
        self.assertEqual(actualMessage, expectedMessage)

    def testSimpleString(self):
        self.parseDump('"abc"', "abc")

    def testStringWithEscapes(self):
        self.parseDump('"a\\"b\\\\c"', "a\"b\\c")

    def testUnterminatedString(self):
        self.expectSyntaxError('"abc', 4, "Unexpected end of file")

    def testTrailingJunk(self):
        self.expectSyntaxError('"abc"xxx', 5, "Expected '+'")

    def testBadEscapeSequence(self):
        self.expectSyntaxError('"ab\\c"', 3, "Bad escape sequence")

    def testStringAddition(self):
        self.parseDump('"abc"+"def"', "abcdef")

    def testStringMultiplication(self):
        self.parseDump('2*"abc"', "abcabc")
        self.parseDump('2*2*"abc"', "abcabcabcabc")
        self.parseDump('2*2*2*"abc"', "abcabcabcabcabcabcabcabc")


if __name__ == "__main__":  # pragma no branch
    unittest.main()
