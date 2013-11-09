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

import MiniParse
import MiniParse.Meta.Grammars.HandWrittenEbnf.Tokens as Tok
from MiniParse.Meta.Grammars.HandWrittenEbnf.Lexer import Lexer


class HandWrittenEbnfLexerTestCase(unittest.TestCase):
    def setUp(self):
        self.lexer = Lexer()

    def lex(self, input, output, positions=None):
        self.assertEqual([t for i, t in self.lexer(input)], output)
        if positions is not None:
            self.assertEqual([i for i, t in self.lexer(input)], positions)

    def testOperators(self):
        self.lex("*", [Tok.Repetition])
        self.lex("-", [Tok.Except])
        self.lex(",", [Tok.Concatenate])
        self.lex("|", [Tok.DefinitionSeparator])
        self.lex("=", [Tok.Defining])
        self.lex(";", [Tok.Terminator])

    def testWhiteSpace(self):
        self.lex(" \n\t\f\r", [])

    def testBracketPairs(self):
        self.lex("(", [Tok.StartGroup])
        self.lex(")", [Tok.EndGroup])
        self.lex("[", [Tok.StartOption])
        self.lex("]", [Tok.EndOption])
        self.lex("{", [Tok.StartRepeat])
        self.lex("}", [Tok.EndRepeat])

    def testTerminal1(self):
        self.lex("'str\"ing'", [Tok.Terminal("""str"ing""")])

    def testTerminal2(self):
        self.lex('"str\'ing"', [Tok.Terminal("""str'ing""")])

    def testComment(self):
        self.lex("(* foo\nbar *)", [])

    def testMetaIdentifier(self):
        self.lex("foo\nbar\tbaz toto", [Tok.MetaIdentifier(["foo", "bar", "baz", "toto"])])

    def testRule(self):
        self.lex(
            "my meta identifier = 100* {[ another meta ], a third meta };",
            [
                Tok.MetaIdentifier(["my", "meta", "identifier"]),
                Tok.Defining,
                Tok.Integer(100),
                Tok.Repetition,
                Tok.StartRepeat,
                Tok.StartOption,
                Tok.MetaIdentifier(["another", "meta"]),
                Tok.EndOption,
                Tok.Concatenate,
                Tok.MetaIdentifier(["a", "third", "meta"]),
                Tok.EndRepeat,
                Tok.Terminator
            ],
            [0, 19, 21, 24, 26, 27, 29, 42, 43, 45, 58, 59]
        )

    def testUnknownChar(self):
        with self.assertRaises(MiniParse.ParsingError) as cm:
            self.lexer("abcd = efgh, ijkl:")
        self.assertEqual(cm.exception.args, ("Unexpected character", 17, set()))

    def testUnclosedString(self):
        with self.assertRaises(MiniParse.ParsingError) as cm:
            self.lexer("abcd = efgh; ' ijkl")
        self.assertEqual(cm.exception.args, ("Unclosed string", 13, set()))

    def testUnclosedComment(self):
        with self.assertRaises(MiniParse.ParsingError) as cm:
            self.lexer("abcd = efgh; (* ijkl")
        self.assertEqual(cm.exception.args, ("Unclosed comment", 13, set()))
