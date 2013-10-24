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


# @todo TODO Understand exactly why the commented code is not needed
class Cursor(object):
    class __BacktrackingInfo:
        def __init__(self, position):
            self.initialPosition = position
            self._maxPosition = position
            self._expected = set()

    def __init__(self, tokens):  # @todo Write tests demonstrating that tokens can be a simple iterator
        self.__tokens = tokens
        self.__position = 0
        self._maxPosition = 0
        self.__value = _NoValue
        self._expected = set()
        self.__backtrackings = []

    @property
    def backtracking(self):
        return Backtracker(self)

    def _pushBacktracking(self):
        self.__backtrackings.append(self.__BacktrackingInfo(self.__position))

    def _popBacktracking(self, failed):
        orig = self.__backtrackings.pop()
        if len(self.__backtrackings) > 0:
            dest = self.__backtrackings[-1]
        else:
            dest = self
        if orig._maxPosition > dest._maxPosition:
            dest._maxPosition = orig._maxPosition
            dest._expected = set(orig._expected)
        elif orig._maxPosition == dest._maxPosition:
            # if len(orig._expected) == 0:
            #     dest._expected = set()
            # else:
                dest._expected.update(orig._expected)
        if failed:
            self.__position = orig.initialPosition
        # @todo if len(self.__backtrackings) == 0: take the opportunity to free the tokens before self.__position: we will never need them again

    @property
    def current(self):
        assert not self.finished
        return self.__tokens[self.__position]

    def advance(self):
        assert not self.finished
        assert len(self.__backtrackings) > 0
        self.__position += 1

    @property
    def finished(self):
        return self.__position == len(self.__tokens)

    def success(self, success):
        if len(self.__backtrackings) > 0:
            bt = self.__backtrackings[-1]
            if self.__position > bt._maxPosition:
                bt._maxPosition = self.__position
                bt._expected = set()
        # else:
        #     if self.__position > self._maxPosition:
        #         self._maxPosition = self.__position
        #         self._expected = set()
        self.__value = success
        return True

    def expected(self, expected):
        assert len(self.__backtrackings) > 0
        # if len(self.__backtrackings) > 0:
        bt = self.__backtrackings[-1]
        assert self.__position == bt._maxPosition
        bt._maxPosition = bt.initialPosition
        bt._expected = set([expected])
        # else:
        #     assert self.__position == self._maxPosition
        #     self._expected = set([expected])
        return self.failure()

    def failure(self):
        self.__value = _NoValue
        return False

    @property
    def error(self):
        assert len(self.__backtrackings) == 0  # @todo Allow consultation of last error before end
        return self._maxPosition, self._expected

    @property
    def value(self):
        assert self.__value is not _NoValue
        return self.__value
