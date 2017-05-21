# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

from .Drawer import Drawer


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
