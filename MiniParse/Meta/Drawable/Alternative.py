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
    radius = 5

    def __init__(self, nodes):
        self.nodes = nodes
        self.extents = []
        self.maxNodeDxRight = 0
        self.totalHeight = 0

    def getExtents(self, ctx):
        self.computeExtents(ctx)

        return (
            4 * self.radius + self.maxNodeDxRight,
            self.extents[0][1],
            self.totalHeight - self.extents[0][1]
        )

    def computeExtents(self, ctx):
        self.extents = []
        self.maxNodeDxRight = 0
        self.totalHeight = self.verticalSpace * (len(self.nodes) - 1)

        for node in self.nodes:
            r, u, d = node.getExtents(ctx)
            self.extents.append((r, u, d))
            self.maxNodeDxRight = max(self.maxNodeDxRight, r)
            self.totalHeight += u + d

    def draw(self, ctx):
        ctx.save()
        self.computeExtents(ctx)

        verticalLineHeight = self.totalHeight - self.extents[0][1] - self.extents[-1][2] - 2 * self.radius

        # Left horizontal line
        ctx.move_to(0, 0)
        ctx.rel_line_to(2 * self.radius, 0)
        # Top-left circle arc
        ctx.move_to(0, 0)
        ctx.arc(0, self.radius, self.radius, 3*math.pi/2, 2*math.pi)
        # Left vertical line
        ctx.move_to(self.radius, self.radius)
        ctx.rel_line_to(0, verticalLineHeight)
        # Right horizontal line
        ctx.move_to(self.maxNodeDxRight + 2 * self.radius, 0)
        ctx.rel_line_to(2 * self.radius, 0)
        # Top-right circle arc
        ctx.move_to(self.maxNodeDxRight + 4 * self.radius, 0)
        ctx.arc_negative(self.maxNodeDxRight + 4 * self.radius, self.radius, self.radius, 3*math.pi/2, math.pi)
        # Right vertical line
        ctx.move_to(self.maxNodeDxRight + 3 * self.radius, self.radius)
        ctx.rel_line_to(0, verticalLineHeight)
        ctx.stroke()

        ctx.translate(2 * self.radius, 0)

        ctx.save()
        self.drawNode(ctx, 0)
        for i in range(len(self.nodes) - 1):
            ctx.translate(0, self.extents[i][2] + self.verticalSpace + self.extents[i][1])
            # Left circle arc
            ctx.move_to(0, 0)
            ctx.arc(0, -self.radius, self.radius, math.pi/2, math.pi)
            # Right circle arc
            ctx.move_to(self.maxNodeDxRight, 0)
            ctx.arc_negative(self.maxNodeDxRight, -self.radius, self.radius, math.pi/2, 0)
            ctx.stroke()
            self.drawNode(ctx, i + 1)
        ctx.restore()

        ctx.restore()

    def drawNode(self, ctx, i):
        dx = (self.maxNodeDxRight - self.extents[i][0]) / 2

        ctx.move_to(0, 0)
        ctx.line_to(dx, 0)
        ctx.move_to(dx + self.extents[i][0], 0)
        ctx.line_to(self.maxNodeDxRight, 0)
        ctx.stroke()

        ctx.save()
        ctx.translate(dx, 0)
        self.nodes[i].draw(ctx)
        ctx.restore()
