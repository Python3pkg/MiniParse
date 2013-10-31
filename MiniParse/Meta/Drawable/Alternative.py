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


class Alternative:
    verticalSpace = 10

    def __init__(self, nodes):
        self.nodes = nodes
        self.extents = []
        self.maxNodeDxRight = 0
        self.totalHeight = 0

    def getExtents(self, drawer):
        self.computeExtents(drawer)

        return (
            2 * drawer.baseLength + self.maxNodeDxRight,
            self.extents[0][1],
            self.totalHeight - self.extents[0][1]
        )

    def computeExtents(self, drawer):
        self.extents = []
        self.maxNodeDxRight = 0
        self.totalHeight = self.verticalSpace * (len(self.nodes) - 1)

        for node in self.nodes:
            r, u, d = node.getExtents(drawer)
            self.extents.append((r, u, d))
            self.maxNodeDxRight = max(self.maxNodeDxRight, r)
            self.totalHeight += u + d

    def draw(self, drawer):
        self.computeExtents(drawer)

        turnLeft, turnRight = drawer.getTurns()

        y = self.extents[0][2]
        for i, node in enumerate(self.nodes[1:]):
            y += self.extents[i + 1][1]
            with drawer.branch:
                turnRight()
                drawer.advance(y)
                turnLeft()
                drawer.advance((self.maxNodeDxRight - self.extents[i + 1][0]) / 2)
                node.draw(drawer)
                drawer.advance((self.maxNodeDxRight - self.extents[i + 1][0]) / 2)
                turnLeft()
                drawer.advance(y)
                turnRight()
            y += self.extents[i + 1][2]
            y += drawer.baseLength
        drawer.advance()
        drawer.advance((self.maxNodeDxRight - self.extents[0][0]) / 2)
        self.nodes[0].draw(drawer)
        drawer.advance((self.maxNodeDxRight - self.extents[0][0]) / 2)
        drawer.advance()
