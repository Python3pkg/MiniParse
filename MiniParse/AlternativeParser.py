# -*- coding: utf-8 -*-

# Copyright 2013 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of MiniParse. http://jacquev6.github.com/MiniParse

# MiniParse is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# MiniParse is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with MiniParse.  If not, see <http://www.gnu.org/licenses/>.


class AlternativeParser:
    def __init__(self, elements, expected=None):
        self.__elements = elements
        self.__expected = expected

    def apply(self, cursor):
        for element in self.__elements:
            if element.apply(cursor):
                return cursor.success(cursor.value)
        if self.__expected is None:
            return cursor.failure()
        else:
            return cursor.expected(self.__expected)
