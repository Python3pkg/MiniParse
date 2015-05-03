# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest

from MiniParse import parse, ParsingError


class ParserTestCase(unittest.TestCase):
    def expectSuccess(self, input, value):
        self.assertEqual(parse(self.p, input), value)

    def expectFailure(self, input, position, expected):
        with self.assertRaises(ParsingError) as cm:
            parse(self.p, input)
        self.assertEqual(cm.exception.message, "Syntax error")
        self.assertEqual(cm.exception.position, position)
        self.assertEqual(cm.exception.expected, set(expected))
