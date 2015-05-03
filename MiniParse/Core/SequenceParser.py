# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>


class SequenceParser:
    def __init__(self, elements, match=None):
        self.__elements = elements
        self.__match = match

    def apply(self, cursor):
        with cursor.backtracking as bt:
            values = []
            for element in self.__elements:
                if element.apply(cursor):
                    values.append(cursor.value)
                else:
                    return bt.failure()
            if self.__match is None:
                return bt.success(tuple(values))
            else:
                return bt.success(self.__match(*values))
