# -*- coding: utf-8 -*-

# Copyright 2013 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of MiniParse. http://jacquev6.github.com/MiniParse

# MiniParse is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# MiniParse is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with MiniParse.  If not, see <http://www.gnu.org/licenses/>.

import MiniParse
import Lexer
import Parser


def parse(builder, input):
    def getLineCol(position):
        before = input[:position]
        lines = before.split("\n")
        return len(lines) - 1, len(lines[-1])

    lex = Lexer.Lexer()
    parse = Parser.Parser(builder)
    try:
        tokens = lex(input)
    except MiniParse.ParsingError, e:
        position = e.position
        raise MiniParse.ParsingError(e.message, getLineCol(position), e.expected)
    try:
        g = parse([t for i, t in tokens])
    except MiniParse.ParsingError, e:
        if e.position < len(tokens):
            position = tokens[e.position][0]
        else:
            position = len(input)
        raise MiniParse.ParsingError(e.message, getLineCol(position), e.expected)
    return g
