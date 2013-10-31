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
from MiniParse.Meta.Syntax import *


class HandWrittenEbnfParserTestCase(unittest.TestCase):
    def parse(self, input, output):
        self.assertEqual(MiniParse.Meta.Grammars.HandWrittenEbnf.parse(input), output)

    def testTerminal(self):
        self.parse("foo = 'bar';", Syntax([SyntaxRule("foo", Terminal("bar"))]))

    def testSeveralRules(self):
        self.parse("foo = 'bar'; foo='baz';", Syntax([SyntaxRule("foo", Terminal("bar")), SyntaxRule("foo", Terminal("baz"))]))

    def testAlternative(self):
        self.parse("foo = 'bar' | 'baz';", Syntax([SyntaxRule("foo", Alternative([Terminal("bar"), Terminal("baz")]))]))

    def testSequence(self):
        self.parse("foo = 'bar', 'baz';", Syntax([SyntaxRule("foo", Sequence([Terminal("bar"), Terminal("baz")]))]))

    def testRepetition(self):
        self.parse("foo = 3 * 'bar';", Syntax([SyntaxRule("foo", Repetition(3, Terminal("bar")))]))

    def testOption(self):
        self.parse("foo = ['bar'];", Syntax([SyntaxRule("foo", Optional(Terminal("bar")))]))

    def testRepeated(self):
        self.parse("foo = {'bar'};", Syntax([SyntaxRule("foo", Repeated(Terminal("bar")))]))

    def testGroup(self):
        self.parse("foo = ('bar');", Syntax([SyntaxRule("foo", Terminal("bar"))]))

    def testNonTerminal(self):
        self.parse("foo = bar;", Syntax([SyntaxRule("foo", NonTerminal("bar"))]))

    def testRestriction(self):
        self.parse("foo = bar - baz;", Syntax([SyntaxRule("foo", Restriction(NonTerminal("bar"), NonTerminal("baz")))]))

    def testGroupedRestriction1(self):
        self.parse("foo = (bar) - (baz);", Syntax([SyntaxRule("foo", Restriction(NonTerminal("bar"), NonTerminal("baz")))]))

    def testGroupedRestriction2(self):
        self.parse(
            "foo = (bar, toto) - (baz | tutu);",
            Syntax([SyntaxRule(
                'foo',
                Restriction(Sequence([NonTerminal('bar'), NonTerminal('toto')]), Alternative([NonTerminal('baz'), NonTerminal('tutu')]))
            )])
        )

    def testEmpty(self):
        self.parse("foo = ;", Syntax([SyntaxRule("foo", Sequence([]))]))

    def testComplexRule(self):
        self.parse(
            "foo = {bar, 'baz', {(2 * 'to', {'tutu'}) | blabla}};",
            Syntax([
                SyntaxRule(
                    'foo',
                    Repeated(
                        Sequence([
                            NonTerminal('bar'),
                            Terminal('baz'),
                            Repeated(
                                Alternative([
                                    Sequence([
                                        Repetition(2, Terminal('to')),
                                        Repeated(Terminal('tutu'))
                                    ]),
                                    NonTerminal('blabla')
                                ])
                            )
                        ])
                    )
                )
            ])
        )
