# -*- coding: utf-8 -*-

# Copyright 2013 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of MiniParse. http://jacquev6.github.com/MiniParse

# MiniParse is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# MiniParse is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with MiniParse.  If not, see <http://www.gnu.org/licenses/>.


class _NoValueType:
    pass
_NoValue = _NoValueType()


class Backtracker:
    def __init__(self, cursor):
        self.__cursor = cursor
        self.__failed = None

    def __enter__(self):
        self.__cursor._pushBacktracking()
        return self

    def __exit__(self, type, exception, traceback):
        if type is None:
            assert self.__failed is not None
            self.__cursor._popBacktracking(self.__failed)

    def success(self, success):
        assert self.__failed is None
        self.__failed = False
        return self.__cursor.success(success)

    def expected(self, expected):
        assert self.__failed is None
        self.__failed = True
        return self.__cursor.expected(expected)

    def failure(self):
        assert self.__failed is None
        self.__failed = True
        return self.__cursor.failure()


class Cursor(object):
    class __BacktrackingInfo:
        def __init__(self, position):
            self.position = position

    def __init__(self, tokens):  # @todo Write tests demonstrating that tokens can be a simple iterator
        self.__tokens = tokens
        self.__position = 0
        self.__maxPosition = 0
        self.__value = _NoValue
        self.__expected = set()
        self.__backtrackings = []

    @property
    def backtracking(self):
        return Backtracker(self)

    def _pushBacktracking(self):
        self.__backtrackings.append(self.__BacktrackingInfo(self.__position))

    def _popBacktracking(self, failed):
        bt = self.__backtrackings.pop()
        if failed:
            self.__position = bt.position
        # @todo if len(self.__backtrackings) == 0: take the opportunity to free the tokens before self.__position: we will never need them again

    @property
    def current(self):
        assert not self.finished
        return self.__tokens[self.__position]

    def advance(self):
        assert not self.finished
        self.__position += 1

    @property
    def finished(self):
        return self.__position == len(self.__tokens)

    def success(self, success):
        if self.__position > self.__maxPosition:
            self.__maxPosition = self.__position
            self.__expected = set()
        self.__value = success
        return True

    def expected(self, expected):
        if self.__position == self.__maxPosition:
            self.__expected.add(expected)
        return self.failure()

    def failure(self):
        self.__value = _NoValue
        return False

    @property
    def error(self):
        return self.__maxPosition, self.__expected

    @property
    def value(self):
        assert self.__value is not _NoValue
        return self.__value
