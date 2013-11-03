# -*- coding: utf-8 -*-

# Copyright 2013 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of MiniParse. http://jacquev6.github.com/MiniParse

# MiniParse is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# MiniParse is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with MiniParse.  If not, see <http://www.gnu.org/licenses/>.

import os
import unittest

import MiniParse.Meta.Grammars.HandWrittenEbnf.Tokens as Tok
import MiniParse.Meta.Grammars.HandWrittenEbnf


class Builder:
    def __getattr__(self, name):
        assert name.startswith("make")
        return lambda *args, **kwds: (name[4:], args, kwds)

b = Builder()


class HandWrittenEbnfParserTestCase(unittest.TestCase):
    def parse(self, input, output):
        self.assertEqual(MiniParse.Meta.Grammars.HandWrittenEbnf.parse(b, input), output)

    def testTerminal(self):
        self.parse("foo = 'bar';", b.makeSyntax([b.makeRule("foo", b.makeTerminal("bar"))]))

    def testSeveralRules(self):
        self.parse("foo = 'bar'; foo='baz';", b.makeSyntax([b.makeRule("foo", b.makeTerminal("bar")), b.makeRule("foo", b.makeTerminal("baz"))]))

    def testAlternative(self):
        self.parse("foo = 'bar' | 'baz';", b.makeSyntax([b.makeRule("foo", b.makeAlternative([b.makeTerminal("bar"), b.makeTerminal("baz")]))]))

    def testSequence(self):
        self.parse("foo = 'bar', 'baz';", b.makeSyntax([b.makeRule("foo", b.makeSequence([b.makeTerminal("bar"), b.makeTerminal("baz")]))]))

    def testRepetition(self):
        self.parse("foo = 3 * 'bar';", b.makeSyntax([b.makeRule("foo", b.makeRepetition(3, b.makeTerminal("bar")))]))

    def testOption(self):
        self.parse("foo = ['bar'];", b.makeSyntax([b.makeRule("foo", b.makeOptional(b.makeTerminal("bar")))]))

    def testRepeated(self):
        self.parse("foo = {'bar'};", b.makeSyntax([b.makeRule("foo", b.makeRepeated(b.makeTerminal("bar")))]))

    def testGroup(self):
        self.parse("foo = ('bar');", b.makeSyntax([b.makeRule("foo", b.makeTerminal("bar"))]))

    def testNonTerminal(self):
        self.parse("foo = bar;", b.makeSyntax([b.makeRule("foo", b.makeNonTerminal("bar"))]))

    def testRestriction(self):
        self.parse("foo = bar - baz;", b.makeSyntax([b.makeRule("foo", b.makeRestriction(b.makeNonTerminal("bar"), b.makeNonTerminal("baz")))]))

    def testGroupedRestriction1(self):
        self.parse("foo = (bar) - (baz);", b.makeSyntax([b.makeRule("foo", b.makeRestriction(b.makeNonTerminal("bar"), b.makeNonTerminal("baz")))]))

    def testGroupedRestriction2(self):
        self.parse(
            "foo = (bar, toto) - (baz | tutu);",
            b.makeSyntax([b.makeRule(
                'foo',
                b.makeRestriction(b.makeSequence([b.makeNonTerminal('bar'), b.makeNonTerminal('toto')]), b.makeAlternative([b.makeNonTerminal('baz'), b.makeNonTerminal('tutu')]))
            )])
        )

    def testEmpty(self):
        self.parse("foo = ;", b.makeSyntax([b.makeRule("foo", b.makeSequence([]))]))

    def testComplexRule(self):
        self.parse(
            "foo = {bar, 'baz', {(2 * 'to', {'tutu'}) | blabla}};",
            b.makeSyntax([
                b.makeRule(
                    'foo',
                    b.makeRepeated(
                        b.makeSequence([
                            b.makeNonTerminal('bar'),
                            b.makeTerminal('baz'),
                            b.makeRepeated(
                                b.makeAlternative([
                                    b.makeSequence([
                                        b.makeRepetition(2, b.makeTerminal('to')),
                                        b.makeRepeated(b.makeTerminal('tutu'))
                                    ]),
                                    b.makeNonTerminal('blabla')
                                ])
                            )
                        ])
                    )
                )
            ])
        )

    def testLexingError(self):
        with self.assertRaises(MiniParse.ParsingError) as cm:
            MiniParse.Meta.Grammars.HandWrittenEbnf.parse(b, "fo =\n'djsj ;")
        self.assertEqual(cm.exception.message, "Unclosed string")
        self.assertEqual(cm.exception.position, (1, 0))
        self.assertEqual(cm.exception.expected, set())

    def testParsingError(self):
        with self.assertRaises(MiniParse.ParsingError) as cm:
            MiniParse.Meta.Grammars.HandWrittenEbnf.parse(b, "fo =\n'djsj',\n'uvw' abc;")
        self.assertEqual(cm.exception.message, "Syntax error")
        self.assertEqual(cm.exception.position, (2, 6))
        self.assertEqual(cm.exception.expected, set([";", "|", ",", "-"]))

    def testParsingErrorAtEndOfInput(self):
        with self.assertRaises(MiniParse.ParsingError) as cm:
            MiniParse.Meta.Grammars.HandWrittenEbnf.parse(b, "fo='djsj'; a")
        self.assertEqual(cm.exception.message, "Syntax error")
        self.assertEqual(cm.exception.position, (0, 12))
        self.assertEqual(cm.exception.expected, set(["="]))
