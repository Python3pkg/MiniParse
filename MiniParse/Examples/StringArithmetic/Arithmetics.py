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
    def __init__(self, terms):
        self.terms = terms

    def dump(self):
        return "".join(t.dump() for t in self.terms)


class StringTerm:
    def __init__(self, rep, factor):
        self.rep = rep
        self.factor = factor

    def dump(self):
        return self.rep.compute() * self.factor.dump()


class IntTerm:
    def __init__(self, factors):
        self.factors = factors

    def compute(self):
        v = 1
        for op, fa in self.factors:
            if op == 1:
                v *= fa.compute()
            else:
                v //= fa.compute()
        return v


class IntExpr:
    def __init__(self, terms):
        self.terms = terms

    def compute(self):
        v = 0
        for op, te in self.terms:
            if op == 1:
                v += te.compute()
            else:
                v -= te.compute()
        return v


class Int:
    def __init__(self, value):
        self.value = value

    def compute(self):
        return self.value


class String:
    def __init__(self, value):
        self.value = value

    def dump(self):
        return self.value
