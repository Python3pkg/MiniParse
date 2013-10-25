from MiniParse import OptionalParser, SequenceParser, AlternativeParser, LiteralParser, RepeatedParser

import Syntax


class StringExprParser:
    @staticmethod
    def apply(cursor):
        return SequenceParser([StringTermParser, RepeatedParser(SequenceParser([LiteralParser('+'), StringTermParser]))], Syntax.StringExpr).apply(cursor)


class StringTermParser:
    @staticmethod
    def apply(cursor):
        return AlternativeParser([RepeatedStringFactorParser, StringFactorParser], Syntax.StringTerm).apply(cursor)


class RepeatedStringFactorParser:
    @staticmethod
    def apply(cursor):
        return SequenceParser([IntTermParser, LiteralParser('*'), StringFactorParser], Syntax.RepeatedStringFactor).apply(cursor)


class StringFactorParser:
    @staticmethod
    def apply(cursor):
        return AlternativeParser([StringParser, SequenceParser([LiteralParser('('), StringExprParser, LiteralParser(')')])], Syntax.StringFactor).apply(cursor)


class IntTermParser:
    @staticmethod
    def apply(cursor):
        return SequenceParser([IntFactorParser, RepeatedParser(SequenceParser([AlternativeParser([LiteralParser('*'), LiteralParser('/')]), IntFactorParser]))], Syntax.IntTerm).apply(cursor)


class IntFactorParser:
    @staticmethod
    def apply(cursor):
        return AlternativeParser([IntParser, SequenceParser([LiteralParser('('), IntExprParser, LiteralParser(')')])], Syntax.IntFactor).apply(cursor)


class IntExprParser:
    @staticmethod
    def apply(cursor):
        return SequenceParser([IntTermParser, RepeatedParser(SequenceParser([AlternativeParser([LiteralParser('+'), LiteralParser('-')]), IntTermParser]))], Syntax.IntExpr).apply(cursor)


class IntParser:
    @staticmethod
    def apply(cursor):
        return SequenceParser([OptionalParser(LiteralParser('-')), DigitParser, RepeatedParser(DigitParser)], Syntax.Int).apply(cursor)


class DigitParser:
    @staticmethod
    def apply(cursor):
        return AlternativeParser([LiteralParser('0'), LiteralParser('1'), LiteralParser('2'), LiteralParser('3'), LiteralParser('4'), LiteralParser('5'), LiteralParser('6'), LiteralParser('7'), LiteralParser('8'), LiteralParser('9')], Syntax.Digit).apply(cursor)


class StringParser:
    @staticmethod
    def apply(cursor):
        return SequenceParser([LiteralParser('"'), RepeatedParser(CharParser), LiteralParser('"')], Syntax.String).apply(cursor)


class CharParser:
    @staticmethod
    def apply(cursor):
        return AlternativeParser([LiteralParser('a'), LiteralParser('b'), LiteralParser('c'), LiteralParser('d'), LiteralParser('e'), LiteralParser('f')], Syntax.Char).apply(cursor)


