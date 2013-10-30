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


class Syntax:
    def __init__(self, rules):
        self.rules = rules

    def getExtents(self, ctx):
        width = 0
        height = 0

        for rule in self.rules:
            w, h = rule.getExtents(ctx)
            width = max(w, width)
            height += 10 + h
        height -= 10

        return width, height

    def draw(self, ctx):
        for rule in self.rules:
            w, h = rule.getExtents(ctx)
            rule.draw(ctx)

            # Debug
            ctx.save()
            ctx.rectangle(0, 0, w, h)
            ctx.set_source_rgba(0, 0, 1, 0.2)
            ctx.fill()
            ctx.restore()

            ctx.translate(0, h + 10)
