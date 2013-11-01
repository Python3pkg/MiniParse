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


class Alternative:
    def __init__(self, nodes):
        self.nodes = nodes

    def getExtents(self, drawer):
        extents, maxNodeDxRight, totalHeight = self.computeExtents(drawer)

        return (
            2 * drawer.baseLength + maxNodeDxRight,
            extents[0][1],
            totalHeight - extents[0][1]
        )

    def computeExtents(self, drawer):
        extents = []
        maxNodeDxRight = 0
        totalHeight = drawer.baseLength * (len(self.nodes) - 1)

        for node in self.nodes:
            r, u, d = node.getExtents(drawer)
            extents.append((r, u, d))
            maxNodeDxRight = max(maxNodeDxRight, r)
            totalHeight += u + d

        return extents, maxNodeDxRight, totalHeight

    def draw(self, drawer):
        extents, maxNodeDxRight, totalHeight = self.computeExtents(drawer)

        turnLeft, turnRight = drawer.getTurns()

        y = extents[0][2]
        for i, node in enumerate(self.nodes[1:]):
            y += extents[i + 1][1]
            with drawer.branch:
                turnRight()
                drawer.advance(y)
                turnLeft()
                drawer.advance((maxNodeDxRight - extents[i + 1][0]) / 2)
                node.draw(drawer)
                drawer.advance((maxNodeDxRight - extents[i + 1][0]) / 2)
                turnLeft()
                drawer.advance(y)
                turnRight()
            y += extents[i + 1][2]
            y += drawer.baseLength
        drawer.advance()
        drawer.advance((maxNodeDxRight - extents[0][0]) / 2)
        self.nodes[0].draw(drawer)
        drawer.advance((maxNodeDxRight - extents[0][0]) / 2)
        drawer.advance()

    def __repr__(self):
        return "Alternative(" + repr(self.nodes) + ")"

    def __eq__(self, other):
        return repr(self) == repr(other)

    def _simplify(self):
        if len(self.nodes) == 1:
            return self.nodes[0]
        else:
            newNodes = []
            for node in self.nodes:
                node = node._simplify()
                if node.__class__ is Alternative:
                    newNodes += node.nodes
                elif any(n == node for n in newNodes):
                    pass
                else:
                    newNodes.append(node)
            return Alternative(newNodes)

    def _getAtomicSuffix(self):
        return self

    def _removeAtomicSuffix(self):
        return Null.Null

    def _getAtomicPrefix(self):
        return self

    def _removeAtomicPrefix(self):
        return Null.Null
