#!/usr/env/bin python
# -*- coding: utf-8 -*-

# Copyright 2013 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of MiniParse. http://jacquev6.github.com/MiniParse

# MiniParse is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# MiniParse is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with MiniParse.  If not, see <http://www.gnu.org/licenses/>.

import sys

import Ebnf.Lexer
import Ebnf.Parser

l = Ebnf.Lexer.Lexer()
p = Ebnf.Parser.Parser()
g = p(l(open(sys.argv[1]).read()))

assert sys.argv[1].endswith(".ebnf")
open(sys.argv[1][:-5] + ".py", "w").write(g.generateMiniParser())
