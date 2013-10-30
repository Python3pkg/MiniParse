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
    labelFontSize = 1.3

    def __init__(self, name, node):
        self.name = name
        self.node = node

    @property
    def label(self):
        return self.name + ":"

    def getExtents(self, drawer):
        r, u, d = self.node.getExtents(drawer)
        width = max(
            drawer.startWidth + r + drawer.stopWidth,
            drawer.getTextWidth(self.label, self.labelFontSize)
        )
        height = drawer.getFontHeight(self.labelFontSize) + u + d
        return width, height

    def draw(self, drawer):
        with drawer.save:
            drawer.drawText(self.label, self.labelFontSize)
            drawer.translateDown(drawer.getFontHeight(self.labelFontSize))

            r, u, d = self.node.getExtents(drawer)
            drawer.translateDown(u)
            drawer.drawStart()
            drawer.translateRight(drawer.startWidth)
            self.node.draw(drawer)
            drawer.translateRight(r)
            drawer.drawStop()
