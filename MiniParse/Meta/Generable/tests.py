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

import MiniParse
from MiniParse.Meta.Generable import builder
from MiniParse.Meta.Grammars.HandWrittenEbnf import parse as parseEbnf


class GenerableIntegrationTestCase(unittest.TestCase):
    def test(self):
        s = parseEbnf(builder, """
            Main = Toto | "titi" | TutuToto | ManyTata | MaybeTete | ThreeTuto | ManyTutaButNotTwo;
            Toto = "toto";
            TutuToto = "tutu", Toto;
            ManyTata = {"tata"};
            MaybeTete = ["tete"];
            ThreeTuto = 3 * "tuto";
            ManyTutaButNotTwo = {"tuta"} - ("tuta", "tuta");
        """)
        code = s.generateMiniParser("Main", computeParserName=lambda rule: rule + "Parser", computeMatchName=lambda rule: "lambda *x: tuple(['" + rule + ":'] + list(x))")
        exec code
        p = Parser()
        self.assertEqual(p(["toto"]), ("Main:", "toto"))
        self.assertEqual(p(["titi"]), ("Main:", "titi"))
        self.assertEqual(p(["tutu", "toto"]), ("Main:", ("TutuToto:", "tutu", "toto")))
        self.assertEqual(p(["tata", "tata", "tata"]), ("Main:", ("ManyTata:", ["tata", "tata", "tata"])))
        # @todo WTF
        # self.assertEqual(p(["tete"]), ("Main:", ("MaybeTete:", "tete")))
        # self.assertEqual(p(["tuto", "tuto", "tuto"]), ())
        # self.assertEqual(p(["tuta", "tuta", "tuta"]), ())
