# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>


class OptionalParser:
    def __init__(self, parser, noMatch=None, match=lambda x: x):
        self.__parser = parser
        self.__noMatch = noMatch
        self.__match = match

    def apply(self, cursor):
        if self.__parser.apply(cursor):
            return cursor.success(self.__match(cursor.value))
        else:
            return cursor.success(self.__noMatch)
