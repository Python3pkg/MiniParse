# -*- coding: utf-8 -*-

# Copyright 2013 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of MiniParse. http://jacquev6.github.com/MiniParse

# MiniParse is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# MiniParse is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with MiniParse.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import cairo
import os

from MiniParse.Meta.Drawable import *


class DrawableTestCase(unittest.TestCase):
    def tearDown(self):
        s = Syntax(self.rules)
        img = cairo.ImageSurface(cairo.FORMAT_RGB24, 1, 1)
        ctx = cairo.Context(img)
        ctx.set_font_size(15)
        w, h = s.getExtents(ctx)
        img = cairo.ImageSurface(cairo.FORMAT_RGB24, int(w) + 10, int(h) + 10)
        ctx = cairo.Context(img)
        ctx.set_font_size(15)
        ctx.set_source_rgb(0.8, 0.8, 0.8)
        ctx.paint()
        ctx.set_source_rgb(1, 1, 1)
        ctx.translate(5, 5)
        ctx.rectangle(0, 0, w, h)
        ctx.fill()
        ctx.set_source_rgb(0, 0, 0)
        s.draw(ctx)
        fileName = os.path.join(
            os.path.dirname(__file__),
            "TestsOutput",
            self.__class__.__name__ + "." + self._testMethodName + ".png"
        )
        img.write_to_png(fileName)

    def testNonTerminal(self):
        self.rules = [
            Rule("non terminal", NonTerminal("in a rectangle"))
        ]

    def testTerminal(self):
        self.rules = [
            Rule("terminal", Terminal("in a rounded rectangle"))
        ]

    def testRuleNamesWithAscentAndDescent(self):
        self.rules = [
            Rule("aaaaa", NonTerminal("ascent and descent")),
            Rule("ppppp", NonTerminal("should")),
            Rule("ddddd", NonTerminal("look")),
            Rule("dddpp", NonTerminal("right"))
        ]

    def testLongRuleName(self):
        self.rules = [
            Rule("this long rule name should not be truncated", NonTerminal("foo 1")),
        ]

    def testAlternative(self):
        self.rules = [
            Rule("alternative", Alternative([
                NonTerminal("with"),
                NonTerminal("several"),
                NonTerminal("branches")
            ]))
        ]

    def testSequence(self):
        self.rules = [
            Rule("sequence", Sequence([
                NonTerminal("with"),
                NonTerminal("one"),
                NonTerminal("branch")
            ]))
        ]

    def testRepetitionWithLongForwardBranch(self):
        self.rules = [
            Rule("repetition", Repetition(
                NonTerminal("forward branch is longer"),
                NonTerminal("backward")
            ))
        ]

    def testRepetitionWithLongBackwardBranch(self):
        self.rules = [
            Rule("repetition", Repetition(
                NonTerminal("forward"),
                NonTerminal("backward branch is longer")
            ))
        ]

    def testImbricatedRepetitions(self):
        self.rules = [
            Rule("repetition", Repetition(
                Repetition(NonTerminal("forward 1"), NonTerminal("backward 1")),
                Repetition(NonTerminal("forward 2"), NonTerminal("backward 2"))
            ))
        ]
