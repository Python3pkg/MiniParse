# -*- coding: utf-8 -*-

# Copyright 2013 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of MiniParse. http://jacquev6.github.com/MiniParse

# MiniParse is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# MiniParse is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with MiniParse.  If not, see <http://www.gnu.org/licenses/>.

import math


class Drawer(object):
    baseLength = 10

    def __init__(self, ctx):
        self.ctx = ctx

    @property
    def __save(self):
        class Restorer:
            def __init__(self, ctx):
                self.ctx = ctx

            def __enter__(self):
                self.ctx.save()

            def __exit__(self, type, exception, stacktrace):
                self.ctx.restore()

        return Restorer(self.ctx)

    @property
    def branch(self):
        class Restorer:
            def __init__(self, ctx):
                self.ctx = ctx

            def __enter__(self):
                self.ctx.save()

            def __exit__(self, type, exception, stacktrace):
                self.ctx.restore()
                self.ctx.move_to(0, 0)

        return Restorer(self.ctx)

    def advance(self, d=baseLength):
        self.ctx.move_to(0, 0)
        self.ctx.rel_line_to(d, 0)
        self.ctx.stroke()
        self.ctx.translate(d, 0)

    def advanceWithArrow(self):
        self.ctx.move_to(0, 0)
        self.ctx.rel_line_to(self.baseLength - 5, 0)
        self.ctx.stroke()
        self.ctx.move_to(self.baseLength - 5.5, -4)
        self.ctx.line_to(self.baseLength - 0.5, 0)
        self.ctx.line_to(self.baseLength - 5.5, 4)
        self.ctx.fill()
        self.ctx.translate(self.baseLength, 0)

    def __turnRight(self):
        self.ctx.move_to(0, 0)
        self.ctx.arc(0, self.baseLength / 2, self.baseLength / 2, 3 * math.pi / 2, 2 * math.pi)
        self.ctx.stroke()
        self.ctx.translate(self.baseLength / 2, self.baseLength / 2)
        self.ctx.rotate(math.pi / 2)

    def __turnLeft(self):
        self.ctx.move_to(0, 0)
        self.ctx.arc_negative(0, -self.baseLength / 2, self.baseLength / 2, math.pi / 2, 0)
        self.ctx.stroke()
        self.ctx.translate(self.baseLength / 2, -self.baseLength / 2)
        self.ctx.rotate(-math.pi / 2)

    def drawStart(self):
        self.ctx.move_to(0, 0)
        self.ctx.arc(self.baseLength / 3, 0, self.baseLength / 3, 0, 2 * math.pi)
        self.ctx.fill()
        self.ctx.move_to(0, 0)
        self.ctx.line_to(self.baseLength, 0)
        self.ctx.stroke()
        self.ctx.translate(self.baseLength, 0)

    def drawStop(self):
        self.ctx.arc(self.baseLength / 2, 0, self.baseLength / 3, 0, 2 * math.pi)
        self.ctx.fill()
        self.ctx.arc(self.baseLength / 2, 0, self.baseLength / 2, 0, 2 * math.pi)
        self.ctx.stroke()
        self.ctx.translate(self.baseLength, 0)

    def drawDeadEnd(self):
        self.ctx.move_to(0, 0)
        self.ctx.line_to(self.baseLength / 2, 0)
        self.ctx.move_to(self.baseLength, self.baseLength / 2)
        self.ctx.line_to(0, -self.baseLength / 2)
        self.ctx.move_to(0, self.baseLength / 2)
        self.ctx.line_to(self.baseLength, -self.baseLength / 2)
        self.ctx.stroke()
        self.ctx.translate(self.baseLength, 0)

    def getTextExtents(self, text, size):
        with self.__save:
            self.ctx.set_font_size(size * 10.)
            x_bearing, y_bearing, width, height, x_advance, y_advance = self.ctx.text_extents(text)
            w = x_advance
            ascent, descent, height, max_x_advance, max_y_advance = self.ctx.font_extents()
            h = height
        return w, h

    def getTextInRectangleExtents(self, text, size):
        w, h = self.getTextExtents(text, size)
        w += self.baseLength
        h += self.baseLength
        return w, h / 2, h / 2

    def drawTextInRectangle(self, text, size):
        r, u, d = self.getTextInRectangleExtents(text, size)
        self.ctx.rectangle(0, -d, r, u + d)
        self.ctx.stroke()
        self.__drawText(self.baseLength / 2, text, size)
        self.ctx.translate(r, 0)

    def getTextInRoundedRectangleExtents(self, text, size):
        w, h = self.getTextExtents(text, size)
        w += 2 * self.baseLength
        h += self.baseLength
        return w, h / 2, h / 2

    def drawTextInRoundedRectangle(self, text, size):
        r, u, d = self.getTextInRoundedRectangleExtents(text, size)
        self.ctx.arc(self.baseLength, 0, self.baseLength, math.pi / 2, -math.pi / 2)
        self.ctx.line_to(r - self.baseLength, -self.baseLength)
        self.ctx.arc(r - self.baseLength, 0, self.baseLength, -math.pi / 2, math.pi / 2)
        self.ctx.line_to(self.baseLength, self.baseLength)
        self.ctx.close_path()
        self.ctx.stroke()
        self.__drawText(self.baseLength, text, size)
        self.ctx.translate(r, 0)

    def __drawText(self, x, text, size):
        w, h = self.getTextExtents(text, size)
        with self.__save:
            if self.__isBackward():
                self.ctx.rotate(math.pi)
                self.ctx.translate(-w - x, 0)
            else:
                self.ctx.translate(x, 0)
            self.ctx.set_font_size(size * 10.)
            ascent, descent, height, max_x_advance, max_y_advance = self.ctx.font_extents()
            self.ctx.move_to(0, (ascent - descent) / 2)
            self.ctx.show_text(text)

    def __isBackward(self):
        xx, yx, xy, yy, x0, y0 = self.ctx.get_matrix()
        return xx < 0

    def getTurns(self):
        if self.__isBackward():
            return self.__turnRight, self.__turnLeft
        else:
            return self.__turnLeft, self.__turnRight
