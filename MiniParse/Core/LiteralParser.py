# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>


class LiteralParser:
    def __init__(self, value, match=None):
        self.__value = value
        self.__match = match or value

    def apply(self, cursor):
        with cursor.backtracking as bt:
            if cursor.finished or cursor.current != self.__value:
                return bt.expected(self.__value)
            else:
                cursor.advance()
                return bt.success(self.__match)
