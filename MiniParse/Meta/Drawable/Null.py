# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>


class __Null:
    def getExtents(self, drawer):
        return 0, 0, 0

    def draw(self, drawer):
        pass

    def __repr__(self):
        return "Null"

    def _simplify(self):
        return self

    def _getAtomicSuffix(self):
        return self

    def _getAtomicPrefix(self):
        return self


Null = __Null()
