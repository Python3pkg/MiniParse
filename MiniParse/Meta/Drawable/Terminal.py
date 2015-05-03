# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

import Null


class Terminal:
    fontSize = 1

    def __init__(self, value):
        self.value = value

    def getExtents(self, drawer):
        r, u, d = drawer.getTextInRoundedRectangleExtents(self.value, self.fontSize)
        return 2 * drawer.baseLength + r, u, d

    def draw(self, drawer):
        drawer.advanceWithArrow()
        drawer.drawTextInRoundedRectangle(self.value, self.fontSize)
        drawer.advance()

    def __repr__(self):
        return "Terminal(" + repr(self.value) + ")"

    def __eq__(self, other):
        return repr(self) == repr(other)

    def _simplify(self):
        return self

    def _getAtomicSuffix(self):
        return self

    def _removeAtomicSuffix(self):
        return Null.Null

    def _getAtomicPrefix(self):
        return self

    def _removeAtomicPrefix(self):
        return Null.Null
