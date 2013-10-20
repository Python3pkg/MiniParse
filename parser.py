#!/usr/bin/env python

import unittest


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


class LiteralParser:
    def __init__(self, value):
        self.__value = value

    def parse(self, c):
        if c.startswith(self.__value):
            c.advance(len(self.__value))
            return ParsingSuccess(self.__value)
        return ParsingFailure("Expected literal <" + self.__value + ">")


class SequenceParser:
    def __init__(self, *elements):
        self.__elements = elements

    def parse(self, c):
        origPos = c.position
        values = []
        for element in self.__elements:
            r = element.parse(c)
            if r.ok:
                values.append(r.value)
            else:
                c.reset(origPos)
                return r
        return ParsingSuccess(values)


class AlternativeParser:
    def __init__(self, *elements):
        self.__elements = elements

    def parse(self, c):
        origPos = c.position
        for element in self.__elements:
            r = element.parse(c)
            if r.ok:
                return r
            else:
                c.reset(origPos)
        return ParsingFailure("Expected something in")


class RepetitionParser:
    def __init__(self, parser):
        self.__parser = parser

    def parse(self, c):
        values = []
        r = self.__parser.parse(c)
        while r.ok:
            values.append(r.value)
            r = self.__parser.parse(c)
        return ParsingSuccess(values)


class ParsingFailure:
    def __init__(self, reason):
        self.ok = False
        self.reason = reason


class ParsingSuccess:
    def __init__(self, value):
        self.ok = True
        self.value = value


class SyntaxError(Exception):
    pass


def parse(s):
    c = Cursor(s)
    r = StringExpr.parse(c)
    if not r.ok:
        raise SyntaxError(c.position, r.reason)
    elif not c.finished:
        raise SyntaxError(c.position, "Expected <+>")
    else:
        return r.value


# Grammar rule: stringExpr = stringTerm, { '+', stringTerm };
class StringExpr:
    def __init__(self, terms):
        self.__terms = terms

    def dump(self):
        return "".join(t.dump() for t in self.__terms)

    @staticmethod
    def parse(c):
        r = SequenceParser(StringTerm, RepetitionParser(SequenceParser(LiteralParser("+"), StringTerm))).parse(c)
        if r:
            terms = [r.value[0]]
            terms += [v[1] for v in r.value[1]]
            return ParsingSuccess(StringExpr(terms))
        else:
            return r


# Grammar rule: stringTerm = [ intTerm, '*' ], stringFactor;
class StringTerm:
    def __init__(self, i, s):
        self.__i = i
        self.__s = s

    def dump(self):
        s = self.__s.dump()
        i = self.__i.compute()
        return i * s

    @staticmethod
    def parse(c):
        # @todo OptionalParser
        rInt = SequenceParser(IntTerm, LiteralParser("*")).parse(c)
        rString = StringFactor.parse(c)
        if rInt.ok and rString.ok:
            return ParsingSuccess(StringTerm(rInt.value[0], rString.value))
        else:
            return rString


# Grammar rule: stringFactor = ( string | '(', stringExpr, ')' );
class StringFactor:
    @staticmethod
    def parse(c):
        return String.parse(c)


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
        r = SequenceParser(IntFactor, RepetitionParser(SequenceParser(LiteralParser("*"), IntFactor))).parse(c)
        if r.ok:
            factors = [r.value[0]]
            factors += [v[1] for v in r.value[1]]
            return ParsingSuccess(IntTerm(factors))
        else:
            return r


# Grammar rule: intFactor = int | '(', intExpr, ')';
class IntFactor:
    @staticmethod
    def parse(c):
        return Int.parse(c)


# Grammar rule: intExpr = intTerm, { ( '+' | '-' ) , intTerm };


# Grammar rule: int = [ '-' ], digit, { digit };
# Grammar rule: digit = '0' | '1' | '...' | '9';
class Int:
    def __init__(self, value):
        self.__value = value

    def compute(self):
        return self.__value

    @staticmethod
    def parse(c):
        digitParser = AlternativeParser(
            LiteralParser("0"),
            LiteralParser("1"),
            LiteralParser("2"),
            LiteralParser("3"),
            LiteralParser("4"),
            LiteralParser("5"),
            LiteralParser("6"),
            LiteralParser("7"),
            LiteralParser("8"),
            LiteralParser("9"),
        )
        r = SequenceParser(digitParser, RepetitionParser(digitParser)).parse(c)
        if r.ok:
            digits = [r.value[0]]
            digits += r.value[1]
            return ParsingSuccess(Int(int("".join(digits))))
        else:
            return r


# Grammar rule: string = '"', { stringElement }, '"';
class String:
    def __init__(self, elements):
        self.__elements = elements

    def dump(self):
        return "".join(e.dump() for e in self.__elements)

    @staticmethod
    def parse(c):
        r = SequenceParser(LiteralParser('"'), RepetitionParser(StringElement), LiteralParser('"')).parse(c)
        if r.ok:
            return ParsingSuccess(String(r.value[1]))
        else:
            return r


# Grammar rule: stringElement = char | escape;
class StringElement:
    @staticmethod
    def parse(c):
        return AlternativeParser(Char, Escape).parse(c)


# Grammar rule: escape = '\"' | '\\';
class Char:
    def __init__(self, value):
        self.__value = value

    def dump(self):
        return self.__value

    @staticmethod
    def parse(c):
        if c.finished:
            raise SyntaxError(c.position, "Unexpected end of file")
        elif c.get(1) in ("\"", "\\"):
            return ParsingFailure("Unexpected <" + c.get(1) + ">")
        else:
            return ParsingSuccess(Char(c.advance(1)))


class Escape:
    def __init__(self, value):
        self.__value = value

    def dump(self):
        return self.__value

    @staticmethod
    def parse(c):
        r = SequenceParser(LiteralParser("\\"), AlternativeParser(LiteralParser("\\"), LiteralParser("\""))).parse(c)
        if r.ok:
            return ParsingSuccess(Escape(r.value[1]))
        elif LiteralParser("\\").parse(c).ok:
            raise SyntaxError(c.position - 1, "Bad escape sequence")
        else:
            return r


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
        self.assertEqual(actualMessage, expectedMessage)
        self.assertEqual(actualPosition, expectedPosition)

    def testSimpleString(self):
        self.parseAndDump('"abc"', "abc")

    def testStringWithEscapes(self):
        self.parseAndDump('"a\\"b\\\\c"', "a\"b\\c")

    def testUnterminatedString(self):
        self.expectSyntaxError('"abc', 4, "Unexpected end of file")

    def testTrailingJunk(self):
        self.expectSyntaxError('"abc"xxx', 5, "Expected <+>")

    def testBadEscapeSequence(self):
        self.expectSyntaxError('"ab\\c"', 3, "Bad escape sequence")

    def testStringAddition(self):
        self.parseAndDump('"abc"+"def"', "abcdef")

    def testStringMultiplication(self):
        self.parseAndDump('2*"abc"', "abcabc")
        self.parseAndDump('2*2*"abc"', "abcabcabcabc")
        self.parseAndDump('2*2*2*"abc"', "abcabcabcabcabcabcabcabc")
        self.parseAndDump('10*"a"', "aaaaaaaaaa")


if __name__ == "__main__":  # pragma no branch
    unittest.main()
