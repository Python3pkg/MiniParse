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


class Drawer(object):
    def __init__(self, ctx):
        self.ctx = ctx

    def translateDown(self, d):
        self.ctx.translate(0, d)

    def translateUp(self, d):
        self.ctx.translate(0, -d)

    def translateRight(self, d):
        self.ctx.translate(d, 0)

    def translateLeft(self, d):
        self.ctx.translate(-d, 0)

    def rotateLeft(self):
        self.ctx.rotate(-math.pi / 2)

    def rotateRight(self):
        self.ctx.rotate(math.pi / 2)

    @property
    def save(self):
        class Restorer:
            def __init__(self, ctx):
                self.ctx = ctx

            def __enter__(self):
                self.ctx.save()

            def __exit__(self, type, exception, stacktrace):
                self.ctx.restore()

        return Restorer(self.ctx)

    segmentLength = 10

    def drawSegment(self):
        with self.save:
            self.ctx.set_source_rgb(0, 1, 0)
            self.ctx.move_to(0, 0)
            self.ctx.rel_line_to(self.segmentLength, 0)
            self.ctx.stroke()

    arrowLength = segmentLength

    def drawArrow(self):
        with self.save:
            self.ctx.set_source_rgb(1, 0, 1)
            self.ctx.move_to(0, 0)
            self.ctx.rel_line_to(self.arrowLength, 0)
            self.ctx.stroke()
            self.ctx.move_to(5, -4)
            self.ctx.line_to(10, 0)
            self.ctx.line_to(5, 4)
            self.ctx.fill()

    arcRadius = segmentLength / 2

    def drawArcRight(self):
        with self.save:
            self.ctx.set_source_rgb(0, 0, 1)
            self.ctx.move_to(0, 0)
            self.ctx.arc(0, self.arcRadius, self.arcRadius, 3 * math.pi / 2, 2 * math.pi)
            self.ctx.stroke()

    def drawArcLeft(self):
        with self.save:
            self.ctx.set_source_rgb(0, 0, 1)
            self.ctx.move_to(0, 0)
            self.ctx.arc_negative(0, -self.arcRadius, self.arcRadius, math.pi / 2, 0)
            self.ctx.stroke()

    startWidth = segmentLength

    def drawStart(self):
        with self.save:
            self.ctx.set_source_rgb(1, 0, 0)
            self.ctx.move_to(0, 0)
            self.ctx.arc(3, 0, 3, 0, 2 * math.pi)
            self.ctx.fill()
            self.ctx.move_to(0, 0)
            self.ctx.line_to(10, 0)
            self.ctx.stroke()

    stopWidth = segmentLength

    def drawStop(self):
        with self.save:
            self.ctx.set_source_rgb(0, 0, 1)
            self.ctx.arc(5, 0, 3, 0, 2 * math.pi)
            self.ctx.fill()
            self.ctx.arc(5, 0, 5, 0, 2 * math.pi)
            self.ctx.stroke()

    def drawLine(self, length):
        with self.save:
            self.ctx.set_source_rgb(0, 1, 1)
            self.ctx.move_to(0, 0)
            self.ctx.line_to(length, 0)
            self.ctx.stroke()

    def getFontHeight(self, size):
        with self.save:
            self.ctx.set_font_size(size * 10.)
            ascent, descent, height, max_x_advance, max_y_advance = self.ctx.font_extents()
            return height

    def getTextWidth(self, text, size):
        with self.save:
            self.ctx.set_font_size(size * 10.)
            x_bearing, y_bearing, width, height, x_advance, y_advance = self.ctx.text_extents(text)
            return width

    def drawText(self, text, size):
        with self.save:
            self.ctx.set_font_size(size * 10.)
            ascent, descent, height, max_x_advance, max_y_advance = self.ctx.font_extents()
            self.translateDown(ascent)
            self.ctx.show_text(text)

    def drawTextVerticallyCentered(self, text, size):
        with self.save:
            self.ctx.set_font_size(size * 10.)
            ascent, descent, height, max_x_advance, max_y_advance = self.ctx.font_extents()
            self.translateDown((ascent - descent) / 2)
            xx, yx, xy, yy, x0, y0 = self.ctx.get_matrix()
            if xx < 0:
                self.ctx.translate(self.getTextWidth(text, size), 0)
                self.ctx.scale(-1, 1)
            self.ctx.show_text(text)
