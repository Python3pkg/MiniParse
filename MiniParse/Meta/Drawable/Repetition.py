# -*- coding: utf-8 -*-

# Copyright 2013 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of MiniParse. http://jacquev6.github.com/MiniParse

# MiniParse is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# MiniParse is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with MiniParse.  If not, see <http://www.gnu.org/licenses/>.

import collections
import math


class Repetition:
    def __init__(self, forward, backward):
        self.forward = forward
        self.backward = backward

    def getExtents(self, drawer):
        forwardRight, forwardUp, forwardDown = self.forward.getExtents(drawer)
        backwardRight, backwardUp, backwardDown = self.backward.getExtents(drawer)

        return (
            max(forwardRight, backwardRight) + 2 * drawer.baseLength,
            forwardUp,
            forwardDown + drawer.baseLength + backwardUp + backwardDown
        )

    def draw(self, drawer):
        forwardRight, forwardUp, forwardDown = self.forward.getExtents(drawer)
        backwardRight, backwardUp, backwardDown = self.backward.getExtents(drawer)

        maxNodeDxRight = max(forwardRight, backwardRight)

        turnLeft, turnRight = drawer.getTurns()

        drawer.advance()
        drawer.advance((maxNodeDxRight - forwardRight) / 2)
        self.forward.draw(drawer)
        drawer.advance((maxNodeDxRight - forwardRight) / 2)
        with drawer.branch:
            turnRight()
            drawer.advance(forwardDown + backwardUp)
            turnRight()
            drawer.advance((maxNodeDxRight - backwardRight) / 2)
            self.backward.draw(drawer)
            drawer.advance((maxNodeDxRight - backwardRight) / 2)
            turnRight()
            drawer.advance(forwardDown + backwardUp)
            turnRight()
        drawer.advance()
