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
    def __init__(self, value, expected=None):
        self.__value = value
        self.__expected = expected

    def parse(self, c):
        origPos = c.position
        for v in self.__value:
            if c.startswith(v):
                c.advance(1)
            else:
                r = ParsingFailure(c.position, self.__expected or ["<" + self.__value + ">"])
                c.reset(origPos)
                return r
        return ParsingSuccess(self.__value, None)


class SequenceParser:
    def __init__(self, elements, expected=None):
        self.__elements = elements
        self.__expected = expected

    def parse(self, c):
        origPos = c.position
        results = []
        for element in self.__elements:
            r = element.parse(c)
            results.append(r)
            if not r.ok:
                c.reset(origPos)
                f = furthestFailure(results)
                if self.__expected is not None:
                    f.expected = self.__expected
                return f
        return ParsingSuccess(tuple(r.value for r in results), furthestFailure(results))


class AlternativeParser:
    def __init__(self, elements, expected=None):
        self.__elements = elements
        self.__expected = expected

    def parse(self, c):
        origPos = c.position
        results = []
        for element in self.__elements:
            r = element.parse(c)
            if r.ok:
                return r
            else:
                c.reset(origPos)
                results.append(r)
        f = furthestFailure(results)
        if self.__expected is not None:
            f.expected = self.__expected
        return f


class RepetitionParser:
    def __init__(self, parser):
        self.__parser = parser

    def parse(self, c):
        results = []
        values = []
        r = self.__parser.parse(c)
        results.append(r)
        while r.ok:
            values.append(r.value)
            r = self.__parser.parse(c)
            results.append(r)
        return ParsingSuccess(values, furthestFailure(results))


class OptionalParser:
    def __init__(self, parser):
        self.__parser = parser

    def parse(self, c):
        r = self.__parser.parse(c)
        if r.ok:
            return r
        else:
            return ParsingSuccess(None, r)


def furthestFailure(results):
    failure = None
    trueFailure = False
    for r in results:
        if r.ok:
            if r.failure is not None:
                if failure is None or r.failure.position > failure.position:
                    failure = r.failure
                    trueFailure = False
                elif r.failure.position == failure.position:
                    failure.expected += r.failure.expected
        else:
            if failure is None or r.position > failure.position or (not trueFailure and r.position >= failure.position):
                failure = r
                trueFailure = True
            elif r.position == failure.position:
                failure.expected += r.expected
    return failure


class ParsingFailure:
    def __init__(self, position, expected):
        self.ok = False
        self.position = position
        self.expected = expected


class ParsingSuccess:
    def __init__(self, value, failure):
        self.ok = True
        self.value = value
        self.failure = failure


class SyntaxError(Exception):
    pass


class ErrorHandling(unittest.TestCase):
    def testErrorComesFromFirstLongestAlternative(self):
        p = AlternativeParser([
            LiteralParser("abx"),
            LiteralParser("abcy"),
            LiteralParser("abcw"),
            LiteralParser("az")
        ])
        r = p.parse(Cursor("abcd"))
        self.assertEqual(r.position, 3)
        self.assertEqual(r.expected, ["<abcy>", "<abcw>"])

    def testLiteralParserTellsWhereItFailed(self):
        p = LiteralParser("abcy")
        r = p.parse(Cursor("abcd"))
        self.assertEqual(r.position, 3)
        self.assertEqual(r.expected, ["<abcy>"])

    def testOptionalParserTellsIfSomethingCouldHaveBeenBetter(self):
        p = OptionalParser(LiteralParser("abcy"))
        r = p.parse(Cursor("abcd"))
        self.assertTrue(r.ok)
        self.assertEqual(r.failure.position, 3)
        self.assertEqual(r.failure.expected, ["<abcy>"])

    def testSequenceStartingWithOptional(self):
        p = SequenceParser([
            OptionalParser(LiteralParser("abcy")),
            LiteralParser("az")
        ])
        r = p.parse(Cursor("abcd"))
        self.assertEqual(r.position, 3)
        self.assertEqual(r.expected, ["<abcy>"])

    def testSequenceParserTellsIfSomethingCouldHaveBeenBetter(self):
        p = SequenceParser([
            OptionalParser(LiteralParser("abcy")),
            LiteralParser("ab")
        ])
        r = p.parse(Cursor("abcd"))
        self.assertEqual(r.failure.position, 3)
        self.assertEqual(r.failure.expected, ["<abcy>"])

    def testSequenceParserTellsIfSomethingCouldHaveBeenBetter_OptionalIsLowerPriorityInCaseOfTie(self):
        p = SequenceParser([
            OptionalParser(LiteralParser("abcy")),
            LiteralParser("abcz")
        ])
        r = p.parse(Cursor("abcd"))
        self.assertEqual(r.position, 3)
        self.assertEqual(r.expected, ["<abcz>"])

    def testRepetitionParserTellsIfSomethingCouldHaveBeenBetter(self):
        p = RepetitionParser(
            SequenceParser([
                OptionalParser(LiteralParser("abcy")),
                LiteralParser("ab")
            ])
        )
        r = p.parse(Cursor("abcd"))
        self.assertEqual(r.failure.position, 3)
        self.assertEqual(r.failure.expected, ["<abcy>"])

    def testRepetitionParserTellsIfSomethingCouldHaveBeenBetter_2(self):
        p = RepetitionParser(
            AlternativeParser([
                LiteralParser("ab"),
                LiteralParser("acd")
            ])
        )
        r = p.parse(Cursor("ababacab"))
        self.assertTrue(r.ok)
        self.assertEqual(r.value, ["ab", "ab"])
        self.assertEqual(r.failure.position, 6)
        self.assertEqual(r.failure.expected, ["<acd>"])

    def testAlternativeParserGivesAllExpectedValues(self):
        p = AlternativeParser([
            AlternativeParser([LiteralParser("xa"), LiteralParser("xb")]),
            AlternativeParser([LiteralParser("xc"), LiteralParser("xd"), LiteralParser("z")])
        ])
        r = p.parse(Cursor("xe"))
        self.assertEqual(r.position, 1)
        self.assertEqual(r.expected, ["<xa>", "<xb>", "<xc>", "<xd>"])


class MinimalArithmeticParserTestCase(unittest.TestCase):
    def setUp(self):
        integer = LiteralParser("1")

        class factor:
            @staticmethod
            def parse(c):
                return AlternativeParser([
                    integer,
                    SequenceParser([
                        LiteralParser("("),
                        expr,
                        LiteralParser(")")
                    ])
                ]).parse(c)

        term = SequenceParser([
            factor,
            RepetitionParser(SequenceParser([
                LiteralParser("*"),
                factor
            ]))
        ])

        expr = SequenceParser([
            term,
            RepetitionParser(SequenceParser([
                LiteralParser("+"),
                term
            ]))
        ])

        self.p = expr

    def testSimpleSuccess(self):
        r = self.p.parse(Cursor("1+1*1"))
        self.assertTrue(r.ok)
        self.assertEqual(
            r.value,
            (  # expr = Seq => tuple
                (  # term = Seq => tuple
                    '1',  # factor = Alt => type of integer => string
                    []  # Rep => list
                ),  # end of term
                [  # Rep => list
                    (  # Seq => tuple
                        '+',  # Lit => string
                        (  # term = Seq => tuple
                            '1',  # factor = Alt => type of integer => string
                            [  # Rep => list
                                (  # Seq => tuple
                                    '*',  # Lit => string
                                    '1'  # factor = Alt => type of integer => string
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertEqual(r.failure.position, 5)
        self.assertEqual(r.failure.expected, ["<+>", "<*>"])

    def testDandlingAdd(self):
        r = self.p.parse(Cursor("1+1+"))
        self.assertEqual(r.failure.position, 4)
        self.assertEqual(r.failure.expected, ["<1>", "<(>"])

    def testDandlingMult(self):
        r = self.p.parse(Cursor("1+1+"))
        self.assertEqual(r.failure.position, 4)
        self.assertEqual(r.failure.expected, ["<1>", "<(>"])

    def testUnclosedParenth(self):
        r = self.p.parse(Cursor("1+(1+1"))
        self.assertEqual(r.failure.position, 6)
        self.assertEqual(r.failure.expected, ["<)>"])


def parse(s):
    c = Cursor(s)
    r = StringExpr.parse(c)
    if not r.ok:
        raise SyntaxError(r.position, "Expected " + " or ".join(r.expected))
    elif not c.finished:
        raise SyntaxError(r.failure.position, "Expected " + " or ".join(r.failure.expected))
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
                RepetitionParser(
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
                v /= f.compute()
        return v

    @staticmethod
    def parse(c):
        r = SequenceParser(
            [
                IntFactor,
                RepetitionParser(
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
                RepetitionParser(
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
                RepetitionParser(Digit)
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
            ["0-9"]
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
                LiteralParser('"', ["opening quote"]),
                RepetitionParser(StringElement),
                LiteralParser('"', ["closing quote"])
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
            ["a-z"]
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
            ["escape sequence"]
        ).parse(c)
        if r.ok:
            return ParsingSuccess(Escape(r.value[1]), r.failure)
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
        self.assertEqual((actualPosition, actualMessage), (expectedPosition, expectedMessage))

    def testSimpleString(self):
        self.parseAndDump('"abc"', "abc")
        self.parseAndDump('"abcdefghijklmnopqrstuvwxyz"', "abcdefghijklmnopqrstuvwxyz")

    def testEmptyInput(self):
        self.expectSyntaxError('', 0, "Expected opening quote or <(>")

    def testForbidenChar(self):
        self.expectSyntaxError('"A"', 1, "Expected closing quote")  # @todo Improve error message

    def testStringWithEscapes(self):
        self.parseAndDump('"a\\"b\\\\c"', "a\"b\\c")

    def testUnterminatedString(self):
        self.expectSyntaxError('"abc', 4, "Expected closing quote")

    def testTrailingJunk(self):
        self.expectSyntaxError('"abc"xxx', 5, "Expected <+>")

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
        self.expectSyntaxError('(1+a)*"abc"', 3, "Expected 0-9 or <(>")

    def testBadAddition_2(self):
        self.expectSyntaxError('(a+1)*"abc"', 1, "Expected opening quote or <(>")

    def testBadStringFactor(self):
        self.expectSyntaxError('(1+1)*a', 6, "Expected opening quote or <(>")

    def testNegativeNumbers(self):
        self.parseAndDump('(2+-1)*"abc"', "abc")

    def testDivision(self):
        self.parseAndDump('(8/4)*"abc"', "abcabc")

    def testSubstraction(self):
        self.parseAndDump('(8-6)*"abc"', "abcabc")

    def testStringExpr(self):
        self.parseAndDump('("abc")', "abc")
        self.parseAndDump('(1+1)*("abc"+"def")', "abcdefabcdef")

    def testBadOperation_1(self):
        self.expectSyntaxError('(1%1)*"a"', 2, "Expected <*>")

    def testBadOperation_2(self):
        self.expectSyntaxError('(1+1%1)*"a"', 4, "Expected <)>")


if __name__ == "__main__":  # pragma no branch
    unittest.main()
