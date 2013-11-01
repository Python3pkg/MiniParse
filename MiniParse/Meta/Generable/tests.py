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
            toto = "toto";
            main = toto | "titi";
        """)
        code = s.generateMiniParser("main", computeParserName=lambda x: x.capitalize() + "Parser", computeMatchName=lambda x: "lambda x: x")
        exec code
        p = Parser()
        self.assertEqual(p(["toto"]), "toto")
        self.assertEqual(p(["titi"]), "titi")
