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
            4 * drawer.arcRadius + self.maxNodeDxRight,
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
        with drawer.save:
            self.computeExtents(drawer)

            verticalLineHeight = self.totalHeight - self.extents[0][1] - self.extents[-1][2] - 2 * drawer.arcRadius

            drawer.drawSegment()
            drawer.drawArcRight()
            with drawer.save:
                drawer.translateRight(drawer.arcRadius)
                drawer.translateDown(drawer.arcRadius)
                drawer.rotateRight()
                drawer.drawLine(verticalLineHeight)

            drawer.translateRight(drawer.arcRadius)

            with drawer.save:
                with drawer.save:
                    drawer.translateRight(drawer.arcRadius)
                    self.drawNode(drawer, 0)
                for i in range(len(self.nodes) - 1):
                    drawer.translateDown(self.extents[i][2] + self.verticalSpace + self.extents[i + 1][1])
                    with drawer.save:
                        drawer.translateUp(drawer.arcRadius)
                        drawer.rotateRight()
                        drawer.drawArcLeft()
                    with drawer.save:
                        drawer.translateRight(drawer.arcRadius)
                        self.drawNode(drawer, i + 1)
                        drawer.translateRight(self.maxNodeDxRight)
                        drawer.drawArcLeft()

            drawer.translateRight(self.maxNodeDxRight + drawer.arcRadius)
            drawer.drawSegment()
            with drawer.save:
                drawer.translateRight(drawer.arcRadius)
                drawer.translateDown(drawer.arcRadius)
                drawer.rotateLeft()
                drawer.drawArcRight()
            with drawer.save:
                drawer.translateRight(drawer.arcRadius)
                drawer.translateDown(drawer.arcRadius)
                drawer.rotateRight()
                drawer.drawLine(verticalLineHeight)

    def drawNode(self, drawer, i):
        with drawer.save:
            dx = (self.maxNodeDxRight - self.extents[i][0]) / 2

            drawer.drawLine(dx)
            drawer.translateRight(dx)
            self.nodes[i].draw(drawer)
            drawer.translateRight(self.extents[i][0])
            drawer.drawLine(dx)
