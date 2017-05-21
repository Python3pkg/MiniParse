# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

from .Cursor import Cursor
from .ParsingError import ParsingError


def parse(parser, tokens):
    c = Cursor(tokens)
    if parser.apply(c):
        if c.finished:
            return c.value
        else:
            raise ParsingError("Syntax error", *c.error)
    else:
        raise ParsingError("Syntax error", *c.error)
