# -*- coding: utf-8 -*-

# Copyright 2013 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of MiniParse. http://jacquev6.github.com/MiniParse

# MiniParse is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# MiniParse is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with MiniParse.  If not, see <http://www.gnu.org/licenses/>.

from Drawer import Drawer


class Rule(object):
    labelFontSize = 1.3

    def __init__(self, name, node):
        self.name = name
        self.node = node

    @property
    def label(self):
        return self.name + ":"

    def getExtents(self, ctx):
        ctx.save()
        ctx.set_font_size(self.labelFontSize * 10)
        ascent, descent, height, max_x_advance, max_y_advance = ctx.font_extents()
        h = ascent + descent
        x_bearing, y_bearing, width, height, x_advance, y_advance = ctx.text_extents(self.label)
        w = x_advance
        ctx.restore()

        drawer = Drawer(ctx)
        r, u, d = self.node.getExtents(drawer)
        return max(w, 2 * drawer.baseLength + r), h + 5 + u + d

    def draw(self, ctx):
        ctx.save()

        ctx.save()
        ctx.set_font_size(self.labelFontSize * 10)
        ascent, descent, height, max_x_advance, max_y_advance = ctx.font_extents()
        ctx.move_to(0, ascent)
        ctx.show_text(self.label)
        ctx.restore()

        ctx.translate(0, ascent + descent + 5)

        drawer = Drawer(ctx)
        r, u, d = self.node.getExtents(drawer)
        ctx.translate(0, u)
        drawer.drawStart()
        self.node.draw(drawer)
        drawer.drawStop()

        ctx.restore()
