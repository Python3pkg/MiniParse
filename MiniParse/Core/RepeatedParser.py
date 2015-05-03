# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>


class RepeatedParser:
    def __init__(self, parser, match=lambda x: x):
        self.__parser = parser
        self.__match = match

    def apply(self, cursor):
        values = []
        while self.__parser.apply(cursor):
            values.append(cursor.value)
        return cursor.success(self.__match(values))
