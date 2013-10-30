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


class Sequence:
    def __init__(self, nodes):
        self.nodes = nodes

    def getExtents(self, ctx):
        right = 0
        up = 0
        down = 0
        for node in self.nodes:
            r, u, d = node.getExtents(ctx)
            right += r
            up = max(up, u)
            down = max(down, d)
        return (right, up, down)

    def draw(self, ctx):
        ctx.save()
        for node in self.nodes:
            r, u, d = node.getExtents(ctx)
            node.draw(ctx)
            ctx.translate(r, 0)
        ctx.restore()
