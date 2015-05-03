# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>


class ParsingError(Exception):
    def __init__(self, message, position, expected):
        Exception.__init__(self, message, position, expected)
        self.message = message
        self.position = position
        self.expected = expected
