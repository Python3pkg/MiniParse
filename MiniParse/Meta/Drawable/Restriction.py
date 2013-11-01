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


class Restriction:
    def __init__(self, base, exception):
        self.base = base
        self.exception = exception

    def getExtents(self, drawer):
        exceptionRight, exceptionUp, exceptionDown = self.exception.getExtents(drawer)
        baseRight, baseUp, baseDown = self.base.getExtents(drawer)

        return (
            max(exceptionRight + drawer.baseLength, baseRight) + 2 * drawer.baseLength,
            exceptionUp,
            exceptionDown + drawer.baseLength + baseUp + baseDown
        )

    def draw(self, drawer):
        exceptionRight, exceptionUp, exceptionDown = self.exception.getExtents(drawer)
        baseRight, baseUp, baseDown = self.base.getExtents(drawer)

        maxNodeDxRight = max(exceptionRight + drawer.baseLength, baseRight)

        turnLeft, turnRight = drawer.getTurns()

        with drawer.branch:
            drawer.advance()
            self.exception.draw(drawer)
            drawer.drawDeadEnd()
        turnRight()
        drawer.advance(exceptionDown + baseUp)
        turnLeft()
        drawer.advance((maxNodeDxRight - baseRight) / 2)
        self.base.draw(drawer)
        drawer.advance((maxNodeDxRight - baseRight) / 2)
        turnLeft()
        drawer.advance(exceptionDown + baseUp)
        turnRight()

    def __repr__(self):
        return "Restriction(" + repr(self.base) + ", " + repr(self.exception) + ")"

    def __eq__(self, other):
        return repr(self) == repr(other)

    def _simplify(self):
        return Restriction(self.base._simplify(), self.exception._simplify())

    def _getAtomicSuffix(self):
        return self

    def _removeAtomicSuffix(self):
        return Null.Null

    def _getAtomicPrefix(self):
        return self

    def _removeAtomicPrefix(self):
        return Null.Null
