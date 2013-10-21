# -*- coding: utf-8 -*-

# Copyright 2013 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of MiniParse. http://jacquev6.github.com/MiniParse

# MiniParse is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# MiniParse is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with MiniParse.  If not, see <http://www.gnu.org/licenses/>.


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
                r = ParsingFailure(c.position, set([self.__expected or "'" + self.__value + "'"]))
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
                    f.expected = set([self.__expected])
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
            f.expected = set([self.__expected])
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
    for result in results:
        f = None
        if result.ok:
            if result.failure is not None:
                f = result.failure
        else:
            f = result
        if f is not None:
            if failure is None or f.position > failure.position:
                failure = f
            if f.position == failure.position:
                failure.expected.update(f.expected)
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
