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

from MiniParse.Meta.Drawable.Syntax import Syntax
from MiniParse.Meta.Drawable.Rule import Rule
from MiniParse.Meta.Drawable.Sequence import Sequence
from MiniParse.Meta.Drawable.Repetition import Repetition
from MiniParse.Meta.Drawable.Alternative import Alternative
from MiniParse.Meta.Drawable.Restriction import Restriction
from MiniParse.Meta.Drawable.NonTerminal import NonTerminal
from MiniParse.Meta.Drawable.Terminal import Terminal
from MiniParse.Meta.Drawable.Null import Null
from MiniParse.Meta.Drawable import builder
from MiniParse.Meta.Grammars.HandWrittenEbnf import parse


def drawSyntaxTo(s, fileName):
    img = cairo.ImageSurface(cairo.FORMAT_RGB24, 1, 1)
    ctx = cairo.Context(img)
    ctx.scale(3, 3)
    w, h = s.getExtents(ctx)
    img = cairo.ImageSurface(cairo.FORMAT_RGB24, 3 * (int(w) + 10), 3 * (int(h) + 10))
    ctx = cairo.Context(img)
    ctx.scale(3, 3)
    ctx.set_source_rgb(0.8, 0.8, 0.8)
    ctx.paint()
    ctx.set_source_rgb(1, 1, 1)
    ctx.translate(5, 5)
    ctx.rectangle(0, 0, w, h)
    ctx.fill()
    ctx.set_source_rgb(0, 0, 0)
    s.draw(ctx)
    img.write_to_png(fileName)


class DrawableTestCase(unittest.TestCase):
    def tearDown(self):
        s = Syntax(self.rules)
        fileName = os.path.join(
            os.path.dirname(__file__),
            "TestsOutput",
            self.__class__.__name__ + "." + self._testMethodName + ".png"
        )
        drawSyntaxTo(s, fileName)

    def testNonTerminal(self):
        self.rules = [
            Rule("non terminal", NonTerminal("in a rectangle"))
        ]

    def testTerminal(self):
        self.rules = [
            Rule("terminal", Terminal("in a rounded rectangle"))
        ]

    def testNull(self):
        self.rules = [
            Rule("sequence with null", Sequence([Terminal("space here ->"), Null, Terminal("should be like here ->"), Terminal("foo")]))
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
            Rule("this long rule name should not be truncated", NonTerminal("foo")),
        ]

    def testAlternative(self):
        self.rules = [
            Rule("alternative", Alternative([
                NonTerminal("with"),
                NonTerminal("several"),
                NonTerminal("branches")
            ]))
        ]

    def testAlternativeWithOneBranch(self):
        self.rules = [
            Rule("alternative", Alternative([
                NonTerminal("with one branch")
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
                Terminal("forward"),
                Terminal("backward branch is longer")
            ))
        ]

    def testImbricatedRepetitions(self):
        self.rules = [
            Rule("repetition", Repetition(
                Repetition(NonTerminal("forward 1"), NonTerminal("backward 1")),
                Repetition(NonTerminal("forward 2"), NonTerminal("backward 2"))
            ))
        ]

    def testBackwardAlternative(self):
        self.rules = [
            Rule("repetition", Repetition(
                NonTerminal("forward"),
                Alternative([
                    NonTerminal("foo"),
                    NonTerminal("bar"),
                    NonTerminal("baz")
                ])
            ))
        ]

    def testRestrictionWithShorterException(self):
        self.rules = [
            Rule("restriction", Restriction(Terminal("long base branch"), Terminal("exception")))
        ]

    def testRestrictionWithLongerException(self):
        self.rules = [
            Rule("restriction", Restriction(Terminal("base"), Terminal("long exception branch")))
        ]


class SimplificationTestCase(unittest.TestCase):
    def testAlternativeWithOneBranch(self):
        a = builder.makeAlternative([Terminal("foo")])
        b = Terminal("foo")
        self.assertEqual(a, b)

    def testAlternativeInAlternative(self):
        a = builder.makeAlternative([Terminal("foo"), Alternative([Terminal("bar"), Terminal("baz")])])
        b = Alternative([Terminal("foo"), Terminal("bar"), Terminal("baz")])
        self.assertEqual(a, b)

    def testDuplicateBranchInAlternative(self):
        a = builder.makeAlternative([Terminal("bar"), Terminal("foo"), Terminal("bar"), Null])
        b = Alternative([Terminal("bar"), Terminal("foo"), Null])
        self.assertEqual(a, b)

    def testMultipleSimplifcationSteps(self):
        a = builder.makeAlternative([Terminal("bar"), Alternative([Terminal("bar"), Terminal("bar")])])
        b = Terminal("bar")
        self.assertEqual(a, b)

    def testEmptySequence(self):
        a = builder.makeSequence([])
        b = Null
        self.assertEqual(a, b)

    def testSequenceWithOneElement(self):
        a = builder.makeSequence([NonTerminal("foo")])
        b = NonTerminal("foo")
        self.assertEqual(a, b)

    def testSequenceInSequence(self):
        a = builder.makeSequence([NonTerminal("foo"), Sequence([Terminal("bar"), Terminal("baz")])])
        b = Sequence([NonTerminal("foo"), Terminal("bar"), Terminal("baz")])
        self.assertEqual(a, b)

    def testNullInSequence(self):
        a = builder.makeSequence([NonTerminal("foo"), Null, Terminal("bar"), Null, Terminal("baz")])
        b = Sequence([NonTerminal("foo"), Terminal("bar"), Terminal("baz")])
        self.assertEqual(a, b)

    def testCommonTerminalBeforeRepetition(self):
        a = builder.makeSequence([Terminal("a"), Repetition(Null, Terminal("a"))])
        b = Repetition(Terminal("a"), Null)
        self.assertEqual(a, b)

    def testCommonNonTerminalBeforeRepetition(self):
        a = builder.makeSequence([NonTerminal("a"), Repetition(Null, NonTerminal("a"))])
        b = Repetition(NonTerminal("a"), Null)
        self.assertEqual(a, b)

    def testCommonSequenceBeforeRepetition(self):
        a = builder.makeSequence([NonTerminal("b"), Terminal("a"), Repetition(Null, Sequence([NonTerminal("b"), Terminal("a")]))])
        b = Repetition(Sequence([NonTerminal("b"), Terminal("a")]), Null)
        self.assertEqual(a, b)

    def testCommonAlternativeBeforeRepetition(self):
        a = builder.makeSequence([Alternative([Terminal("d"), Terminal("e")]), Repetition(Null, Alternative([Terminal("d"), Terminal("e")]))])
        b = Repetition(Alternative([Terminal("d"), Terminal("e")]), Null)
        self.assertEqual(a, b)

    def testCommonRepetitionBeforeRepetition(self):
        a = builder.makeSequence([Repetition(Terminal("d"), Terminal("e")), Repetition(Null, Repetition(Terminal("d"), Terminal("e")))])
        b = Repetition(Repetition(Terminal("d"), Terminal("e")), Null)
        self.assertEqual(a, b)

    def testCommonRestrictionBeforeRepetition(self):
        a = builder.makeSequence([Restriction(Terminal("d"), Terminal("e")), Repetition(Null, Restriction(Terminal("d"), Terminal("e")))])
        b = Repetition(Restriction(Terminal("d"), Terminal("e")), Null)
        self.assertEqual(a, b)

    def testNoCommonNullBeforeRepetition(self):
        a = builder.makeSequence([Terminal("d"), Repetition(NonTerminal("b"), Null)])
        b = Sequence([Terminal("d"), Repetition(NonTerminal("b"), Null)])
        self.assertEqual(a, b)

    def testCommonTerminalAfterRepetition(self):
        a = builder.makeSequence([Repetition(Null, Terminal("a")), Terminal("a")])
        b = Repetition(Terminal("a"), Null)
        self.assertEqual(a, b)

    def testCommonNonTerminalAfterRepetition(self):
        a = builder.makeSequence([Repetition(Null, NonTerminal("a")), NonTerminal("a")])
        b = Repetition(NonTerminal("a"), Null)
        self.assertEqual(a, b)

    def testCommonSequenceAfterRepetition(self):
        a = builder.makeSequence([Repetition(Null, Sequence([NonTerminal("b"), Terminal("a")])), NonTerminal("b"), Terminal("a")])
        b = Repetition(Sequence([NonTerminal("b"), Terminal("a")]), Null)
        self.assertEqual(a, b)

    def testCommonAlternativeAfterRepetition(self):
        a = builder.makeSequence([Repetition(Null, Alternative([Terminal("d"), Terminal("e")])), Alternative([Terminal("d"), Terminal("e")])])
        b = Repetition(Alternative([Terminal("d"), Terminal("e")]), Null)
        self.assertEqual(a, b)

    def testCommonRepetitionAfterRepetition(self):
        a = builder.makeSequence([Repetition(Null, Repetition(Terminal("d"), Terminal("e"))), Repetition(Terminal("d"), Terminal("e"))])
        b = Repetition(Repetition(Terminal("d"), Terminal("e")), Null)
        self.assertEqual(a, b)

    def testCommonRestrictionAfterRepetition(self):
        a = builder.makeSequence([Repetition(Null, Restriction(Terminal("d"), Terminal("e"))), Restriction(Terminal("d"), Terminal("e"))])
        b = Repetition(Restriction(Terminal("d"), Terminal("e")), Null)
        self.assertEqual(a, b)

    def testNoCommonNullAfterRepetition(self):
        a = builder.makeSequence([Repetition(NonTerminal("b"), Null), Terminal("d")])
        b = Sequence([Repetition(NonTerminal("b"), Null), Terminal("d")])
        self.assertEqual(a, b)


class DrawingIntegrationTestCase(unittest.TestCase):
    def test(self):
        s = parse(builder, """
            rule1 = { rule2 }, 3 * "foo", "bar";
            rule2 = [ "baz" ], ( "xxx" | "yyy", , , "zzz" ), ("foo" - "bar");
        """)
        fileName = os.path.join(
            os.path.dirname(__file__),
            "TestsOutput",
            self.__class__.__name__ + "." + self._testMethodName + ".png"
        )
        drawSyntaxTo(s, fileName)
