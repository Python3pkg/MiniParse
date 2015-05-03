# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>


import Arithmetics


def makeStringExpr(term, terms):
    return Arithmetics.StringExpr([term] + [t for (plus, t) in terms])


def makeStringTerm(rep, factor):
    if rep is None:
        return factor
    else:
        rep, mult = rep
        return Arithmetics.StringTerm(rep, factor)


def makeStringFactor(factor):
    if isinstance(factor, tuple):
        leftPar, factor, rightPar = factor
    return factor


def makeString(openingQuote, chars, closingQuote):
    return Arithmetics.String("".join(chars))


def makeChar(value):
    return value


def makeIntTerm(factor, factors):
    return Arithmetics.IntTerm([(1, factor)] + [(1 if op == "*" else -1, fa) for (op, fa) in factors])


def makeIntFactor(factor):
    if not isinstance(factor, Arithmetics.Int):
        leftPar, factor, rightPar = factor
    return factor


def makeIntExpr(term, terms):
    return Arithmetics.IntExpr([(1, term)] + [(1 if op == "+" else -1, te) for (op, te) in terms])


def makeInt(sign, digit, digits):
    sign = 1 if sign is None else -1
    digits = [digit] + digits
    return Arithmetics.Int(sign * int("".join(digits)))


def makeDigit(value):
    return value
