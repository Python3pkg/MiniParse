# -*- coding: utf-8 -*-

# Copyright 2013 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of MiniParse. http://jacquev6.github.com/MiniParse

# MiniParse is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# MiniParse is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with MiniParse.  If not, see <http://www.gnu.org/licenses/>.


class SequenceParser:
    def __init__(self, elements, expected=None, match=lambda x: x):
        self.__elements = elements
        self.__expected = expected
        self.__match = match

    def apply(self, cursor):
        with cursor.backtracking as bt:
            values = []
            for element in self.__elements:
                if element.apply(cursor):
                    values.append(cursor.value)
                else:
                    if self.__expected is None:
                        return bt.failure()
                    else:
                        return bt.expected(self.__expected)
            return bt.success(self.__match(tuple(values)))
