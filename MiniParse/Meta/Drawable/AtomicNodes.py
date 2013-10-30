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


DrawingExtents = collections.namedtuple("DrawingExtents", "right,up,down")
# x_bearing, y_bearing, width, height, x_advance, y_advance = ctx.text_extents(text)
TextExtents = collections.namedtuple("TextExtents", "x_bearing,y_bearing,width,height,x_advance,y_advance")
# ascent, descent, height, max_x_advance, max_y_advance = ctx.font_extents()
# xx, yx, xy, yy, x0, y0 = ctx.get_matrix()


def deltaForVerticalTextCentering(ctx):
    ascent, descent, height, max_x_advance, max_y_advance = ctx.font_extents()
    return (ascent - descent) / 2


def textHeight(ctx):
    ascent, descent, height, max_x_advance, max_y_advance = ctx.font_extents()
    return ascent + descent


class _AtomicValuedNode:
    def __init__(self, value):
        self.value = value
        textExtents = None
        horizontalMargin = 0
        verticalMargin = 0

    def getExtents(self, ctx):
        self.computeExtents(ctx)

        height = textHeight(ctx) + self.verticalMargin
        return (
            self.textExtents.x_advance + self.horizontalMargin + 20,
            height / 2,
            height / 2
        )

    def draw(self, ctx):
        ctx.save()
        self.computeExtents(ctx)

        ctx.move_to(0, 0)
        ctx.line_to(10, 0)
        ctx.move_to(self.textExtents.x_advance + self.horizontalMargin + 10, 0)
        ctx.line_to(self.textExtents.x_advance + self.horizontalMargin + 20, 0)
        ctx.stroke()
        ctx.move_to(5, -4)
        ctx.line_to(10, 0)
        ctx.line_to(5, 4)
        ctx.fill()

        ctx.translate(10, 0)

        # Text
        ctx.save()
        ctx.translate(self.horizontalMargin/2, deltaForVerticalTextCentering(ctx))
        xx, yx, xy, yy, x0, y0 = ctx.get_matrix()
        if xx < 0:
            ctx.translate(self.textExtents.x_advance, 0)
            ctx.scale(-1, 1)
        ctx.show_text(self.value)
        ctx.restore()

        width = self.textExtents.x_advance + self.horizontalMargin
        height = textHeight(ctx) + self.verticalMargin
        ctx.translate(0, -height / 2)
        self.drawSurroundingShape(ctx, width, height)
        ctx.stroke()
        ctx.restore()


class NonTerminal(_AtomicValuedNode):
    def __init__(self, value):
        _AtomicValuedNode.__init__(self, value)

    def computeExtents(self, ctx):
        self.verticalMargin = 10
        self.horizontalMargin = 10
        self.textExtents = TextExtents(*ctx.text_extents(self.value))

    def drawSurroundingShape(self, ctx, width, height):
        ctx.rectangle(0, 0, width, height)


class Terminal(_AtomicValuedNode):
    def __init__(self, value):
        _AtomicValuedNode.__init__(self, value)

    def computeExtents(self, ctx):
        self.verticalMargin = 10
        self.horizontalMargin = 10
        self.textExtents = TextExtents(*ctx.text_extents(self.value))

    def drawSurroundingShape(self, ctx, width, height):
        ctx.move_to(height / 2, 0)
        ctx.line_to(width - height / 2, 0)
        ctx.arc(width - height / 2, height / 2, height / 2, -math.pi / 2, math.pi / 2)
        ctx.line_to(height / 2, height)
        ctx.arc(height / 2, height / 2, height / 2, math.pi / 2, -math.pi / 2)
