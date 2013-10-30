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
    radius = 5
    verticalSpace = 10

    def __init__(self, forward, backward):
        self.forward = forward
        self.backward = backward

    def getExtents(self, ctx):
        forwardRight, forwardUp, forwardDown = self.forward.getExtents(ctx)
        backwardRight, backwardUp, backwardDown = self.backward.getExtents(ctx)

        return (
            max(forwardRight, backwardRight) + 4 * self.radius,
            forwardUp,
            forwardDown + self.verticalSpace + backwardUp + backwardDown
        )

    def draw(self, ctx):
        ctx.save()
        forwardRight, forwardUp, forwardDown = self.forward.getExtents(ctx)
        backwardRight, backwardUp, backwardDown = self.backward.getExtents(ctx)

        maxNodeDxRight = max(forwardRight, backwardRight)

        # Top-left horizontal line
        ctx.move_to(0, 0)
        ctx.line_to(2 * self.radius + (maxNodeDxRight - forwardRight) / 2, 0)
        ctx.stroke()

        # Forward
        ctx.save()
        ctx.translate(2 * self.radius + (maxNodeDxRight - forwardRight) / 2, 0)
        self.forward.draw(ctx)
        ctx.restore()

        # Top-right horizontal line
        ctx.move_to(2 * self.radius + (maxNodeDxRight + forwardRight) / 2, 0)
        ctx.line_to(maxNodeDxRight + 4 * self.radius, 0)
        ctx.stroke()

        # Right half-circle
        ctx.move_to(2 * self.radius + maxNodeDxRight, 0)
        ctx.arc(2 * self.radius + maxNodeDxRight, self.radius, self.radius, 3 * math.pi / 2, 2 * math.pi)
        ctx.line_to(3 * self.radius + maxNodeDxRight, forwardDown + self.verticalSpace + backwardUp - self.radius)
        ctx.arc(2 * self.radius + maxNodeDxRight, forwardDown + self.verticalSpace + backwardUp - self.radius, self.radius, 0, math.pi / 2)
        # Bottom-right horizontal line
        ctx.line_to(2 * self.radius + (maxNodeDxRight + backwardRight) / 2, forwardDown + self.verticalSpace + backwardUp)
        ctx.stroke()

        # Backward
        ctx.save()
        ctx.translate(2 * self.radius + (maxNodeDxRight + backwardRight) / 2, forwardDown + self.verticalSpace + backwardUp)
        ctx.scale(-1, 1)
        self.backward.draw(ctx)
        ctx.restore()

        # Bottom-left horizontal line
        ctx.move_to(2 * self.radius + (maxNodeDxRight - backwardRight) / 2, forwardDown + self.verticalSpace + backwardUp)
        ctx.line_to(2 * self.radius, forwardDown + self.verticalSpace + backwardUp)
        # Left half-circle
        ctx.arc(2 * self.radius, forwardDown + self.verticalSpace + backwardUp - self.radius, self.radius, math.pi / 2, math.pi)
        ctx.line_to(self.radius, self.radius)
        ctx.arc(2 * self.radius, self.radius, self.radius, math.pi, 3 * math.pi / 2)
        ctx.stroke()

        ctx.restore()
