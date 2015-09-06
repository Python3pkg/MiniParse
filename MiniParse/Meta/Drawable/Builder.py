# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

from Syntax import Syntax
from Rule import Rule
from Alternative import Alternative
from Sequence import Sequence
from Repetition import Repetition
from Terminal import Terminal
from NonTerminal import NonTerminal
from Restriction import Restriction
from Null import Null


class Builder:
    def makeSyntax(self, rules):
        return Syntax(rules)

    def makeRule(self, name, d):
        return Rule(name, d)

    def makeAlternative(self, elems):
        return self.__simplify(Alternative(elems))

    def makeSequence(self, elems):
        return self.__simplify(Sequence(elems))

    def makeRepeated(self, x):
        return self.__simplify(Repetition(Null, x))

    def makeOptional(self, x):
        return self.__simplify(Alternative([Null, x]))

    def makeTerminal(self, value):
        return self.__simplify(Terminal(value))

    def makeNonTerminal(self, value):
        return self.__simplify(NonTerminal(value))

    def makeRepetition(self, n, x):
        # @todo Draw the number of repetitions (n)
        return self.__simplify(Repetition(x, Null))

    def makeRestriction(self, base, exception):
        return self.__simplify(Restriction(base, exception))

    def __simplify(self, node):
        newNode = node._simplify()
        while not newNode == node:
            node = newNode
            newNode = node._simplify()
        return newNode
