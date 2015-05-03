# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

from Syntax import *


class Builder:
    def makeSyntax(self, rules):
        return Syntax(rules)

    def makeRule(self, name, d):
        return Rule(name, d)

    def makeAlternative(self, elems):
        return Alternative(elems)

    def makeSequence(self, elems):
        return Sequence(elems)

    def makeRepeated(self, x):
        return Repeated(x)

    def makeOptional(self, x):
        return Optional(x)

    def makeTerminal(self, value):
        return Terminal(value)

    def makeNonTerminal(self, value):
        return NonTerminal(value)

    def makeRepetition(self, n, x):
        return Repetition(n, x)

    def makeRestriction(self, b, x):
        return Restriction(b, x)


builder = Builder()
