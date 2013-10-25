# -*- coding: utf-8 -*-

# Copyright 2013 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of MiniParse. http://jacquev6.github.com/MiniParse

# MiniParse is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# MiniParse is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with MiniParse.  If not, see <http://www.gnu.org/licenses/>.


class StringExpr:
    def __init__(self, term, terms):
        self.terms = [term] + [t for (plus, t) in terms]

    def dump(self):
        return "".join(t.dump() for t in self.terms)


def StringTerm(term):
    return term


class RepeatedStringFactor:
    def __init__(self, rep, times, factor):
        self.rep = rep
        self.factor = factor

    def dump(self):
        return self.rep.compute() * self.factor.dump()


def StringFactor(factor):
    if not isinstance(factor, String):
        leftPar, factor, rightPar = factor
    return factor


class IntTerm:
    def __init__(self, factor, factors):
        self.factors = [(1, factor)] + [(1 if op == "*" else -1, fa) for (op, fa) in factors]

    def compute(self):
        v = 1
        for op, fa in self.factors:
            if op == 1:
                v *= fa.compute()
            else:
                v //= fa.compute()
        return v


def IntFactor(factor):
    if not isinstance(factor, Int):
        leftPar, factor, rightPar = factor
    return factor


class IntExpr:
    def __init__(self, term, terms):
        self.terms = [(1, term)] + [(1 if op == "+" else -1, te) for (op, te) in terms]

    def compute(self):
        v = 0
        for op, te in self.terms:
            if op == 1:
                v += te.compute()
            else:
                v -= te.compute()
        return v


class Int:
    def __init__(self, sign, digit, digits):
        sign = 1 if sign is None else -1
        digits = [digit] + digits
        self.value = sign * int("".join(digits))

    def compute(self):
        return self.value


def Digit(value):
    return value


class String:
    def __init__(self, openingQuote, chars, closingQuote):
        self.value = "".join(chars)

    def dump(self):
        return self.value


def Char(value):
    return value
