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
    class Backtracking(object):
        def __init__(self, cursor):
            self.__cursor = cursor
            self.__ended = False

        def __enter__(self, *args):
            return self

        def __exit__(self, *args):
            assert self.__ended

        @property
        def next(self):
            return self.__cursor._next()

        def success(self, value):
            self.__end()
            return self.__cursor._success(value)

        def expected(self, expected):
            self.__end()
            return self.__cursor._expected(expected)

        def failure(self):
            self.__end()
            return self.__cursor._failure()

        def __end(self):
            assert not self.__ended
            self.__ended = True

    def __init__(self, tokens):  # @todo Write tests demonstrating that tokens can be a simple iterator
        self.__tokens = tokens
        self.__position = 0
        self.__maxPosition = 0
        self.__expected = set()

    @property
    def backtracking(self):
        return Cursor.Backtracking(self)

    def _next(self):
        next = self.__tokens[self.__position]
        self.__position += 1
        return next

    def _success(self, value):
        if self.__position >= self.__maxPosition:
            self.__maxPosition = self.__position
            self.__expected = set()
        self.value = value
        return True

    def _expected(self, expected):
        if self.__position > self.__maxPosition:
            self.__expected.add(expected)
        return False

    def _failure(self):
        return False

    @property
    def error(self):
        return self.__maxPosition, self.__expected

    @property
    def finished(self):
        return self.__position == len(self.__tokens)
