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


class Rule(object):
    def __init__(self, name, node):
        self.name = name
        self.node = node

    @property
    def label(self):
        return self.name + ":"

    def getExtents(self, ctx):
        r, u, d = self.node.getExtents(ctx)
        x_bearing, y_bearing, width, height, x_advance, y_advance = ctx.text_extents(self.label)
        w = max(50 + 10 + r + 10, x_advance)
        ascent, descent, height, max_x_advance, max_y_advance = ctx.font_extents()
        h = height + u + d
        return w, h

    def draw(self, ctx):
        ctx.save()

        x_bearing, y_bearing, width, height, x_advance, y_advance = ctx.text_extents(self.label)
        ascent, descent, height, max_x_advance, max_y_advance = ctx.font_extents()
        ctx.translate(0, ascent)
        ctx.show_text(self.label)

        # Debug
        ctx.save()
        ctx.rectangle(0, -ascent, width, height)
        ctx.set_source_rgba(1, 0, 0, 0.2)
        ctx.fill()
        ctx.restore()

        r, u, d = self.node.getExtents(ctx)
        ctx.translate(50, descent + u)

        # Start circle
        ctx.arc(3, 0, 3, 0, 2 * math.pi)
        ctx.fill()
        # Start line
        ctx.line_to(6, 0)
        ctx.line_to(10, 0)
        ctx.stroke()

        # Node
        ctx.translate(10, 0)
        self.node.draw(ctx)

        # Debug
        ctx.save()
        ctx.rectangle(0, -u, r, u + d)
        ctx.set_source_rgba(1, 0, 0, 0.2)
        ctx.fill()
        ctx.restore()

        # Stop circle
        ctx.translate(r, 0)
        ctx.arc(5, 0, 3, 0, 2 * math.pi)
        ctx.fill()
        ctx.arc(5, 0, 5, 0, 2 * math.pi)
        ctx.stroke()

        ctx.restore()
