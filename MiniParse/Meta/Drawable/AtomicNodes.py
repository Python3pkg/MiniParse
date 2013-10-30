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


class _AtomicValuedNode:
    verticalMargin = 10
    horizontalMargin = 10
    fontSize = 1

    def __init__(self, value):
        self.value = value

    def getExtents(self, drawer):
        height = drawer.getFontHeight(self.fontSize) + self.verticalMargin
        return (
            drawer.arrowLength + drawer.getTextWidth(self.value, self.fontSize) + self.horizontalMargin + drawer.segmentLength,
            height / 2,
            height / 2
        )

    def draw(self, drawer):
        textWidth = drawer.getTextWidth(self.value, self.fontSize)
        with drawer.save:
            drawer.drawArrow()

            drawer.translateRight(drawer.arrowLength)

            with drawer.save:
                drawer.translateRight(self.horizontalMargin / 2)
                drawer.drawTextVerticallyCentered(self.value, self.fontSize)

            width = textWidth + self.horizontalMargin
            height = drawer.getFontHeight(self.fontSize) + self.verticalMargin
            with drawer.save:
                drawer.translateDown(-height / 2)
                self.drawSurroundingShape(drawer, width, height)

            drawer.translateRight(textWidth + self.horizontalMargin)
            drawer.drawSegment()


class NonTerminal(_AtomicValuedNode):
    def drawSurroundingShape(self, drawer, width, height):
        drawer.ctx.rectangle(0, 0, width, height)
        drawer.ctx.stroke()


class Terminal(_AtomicValuedNode):
    def drawSurroundingShape(self, drawer, width, height):
        drawer.ctx.move_to(height / 2, 0)
        drawer.ctx.line_to(width - height / 2, 0)
        drawer.ctx.arc(width - height / 2, height / 2, height / 2, -math.pi / 2, math.pi / 2)
        drawer.ctx.line_to(height / 2, height)
        drawer.ctx.arc(height / 2, height / 2, height / 2, math.pi / 2, -math.pi / 2)
        drawer.ctx.stroke()
