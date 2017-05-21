# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

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
        globs = {"MiniParse": MiniParse}
        exec(code, globs)
        Parser = globs["Parser"]
        p = Parser()
        self.assertEqual(p(["toto"]), ("Main:", "toto"))
        self.assertEqual(p(["titi"]), ("Main:", "titi"))
        self.assertEqual(p(["tutu", "toto"]), ("Main:", ("TutuToto:", "tutu", "toto")))
        self.assertEqual(p(["tata", "tata", "tata"]), ("Main:", ("ManyTata:", ["tata", "tata", "tata"])))
        # @todo WTF
        # self.assertEqual(p(["tete"]), ("Main:", ("MaybeTete:", "tete")))
        # self.assertEqual(p(["tuto", "tuto", "tuto"]), ())
        # self.assertEqual(p(["tuta", "tuta", "tuta"]), ())
