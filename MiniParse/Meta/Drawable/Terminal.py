# -*- coding: utf-8 -*-

# Copyright 2013 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of MiniParse. http://jacquev6.github.com/MiniParse

# MiniParse is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# MiniParse is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with MiniParse.  If not, see <http://www.gnu.org/licenses/>.

import Null


class Terminal:
    fontSize = 1

    def __init__(self, value):
        self.value = value

    def getExtents(self, drawer):
        r, u, d = drawer.getTextInRoundedRectangleExtents(self.value, self.fontSize)
        return 2 * drawer.baseLength + r, u, d

    def draw(self, drawer):
        drawer.advanceWithArrow()
        drawer.drawTextInRoundedRectangle(self.value, self.fontSize)
        drawer.advance()

    def __repr__(self):
        return "Terminal(" + repr(self.value) + ")"

    def __eq__(self, other):
        return repr(self) == repr(other)

    def _simplify(self):
        return self

    def _getAtomicSuffix(self):
        return self

    def _removeAtomicSuffix(self):
        return Null.Null

    def _getAtomicPrefix(self):
        return self

    def _removeAtomicPrefix(self):
        return Null.Null
