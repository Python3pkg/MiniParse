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

from Drawer import Drawer


class Syntax:
    def __init__(self, rules):
        self.rules = rules

    def getExtents(self, ctx):
        drawer = Drawer(ctx)

        width = 0
        height = 0

        for rule in self.rules:
            w, h = rule.getExtents(drawer)
            width = max(w, width)
            height += 10 + h
        height -= 10

        return width, height

    def draw(self, ctx):
        drawer = Drawer(ctx)

        for rule in self.rules:
            w, h = rule.getExtents(drawer)
            rule.draw(drawer)
            drawer.translateDown(h + 10)
