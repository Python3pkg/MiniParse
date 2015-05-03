# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>


class AlternativeParser:
    def __init__(self, elements, match=lambda x: x):
        self.__elements = elements
        self.__match = match

    def apply(self, cursor):
        with cursor.backtracking as bt:  # @todo Here, we need backtracking only because of self.__expected.
            for element in self.__elements:
                if element.apply(cursor):
                    return bt.success(self.__match(cursor.value))
            return bt.failure()
