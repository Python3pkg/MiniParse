# -*- coding: utf-8 -*-

# Copyright 2013 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of MiniParse. http://jacquev6.github.com/MiniParse

# MiniParse is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# MiniParse is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with MiniParse.  If not, see <http://www.gnu.org/licenses/>.

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
