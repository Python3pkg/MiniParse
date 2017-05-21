# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

import MiniParse
from . import Lexer
from . import Parser


def parse(builder, input):
    def getLineCol(position):
        before = input[:position]
        lines = before.split("\n")
        return len(lines) - 1, len(lines[-1])

    lex = Lexer.Lexer()
    parse = Parser.Parser(builder)
    try:
        tokens = lex(input)
    except MiniParse.ParsingError as e:
        position = e.position
        raise MiniParse.ParsingError(e.message, getLineCol(position), e.expected)
    try:
        g = parse([t for i, t in tokens])
    except MiniParse.ParsingError as e:
        if e.position < len(tokens):
            position = tokens[e.position][0]
        else:
            position = len(input)
        raise MiniParse.ParsingError(e.message, getLineCol(position), e.expected)
    return g
