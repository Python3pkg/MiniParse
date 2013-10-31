# -*- coding: utf-8 -*-

# Copyright 2013 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of MiniParse. http://jacquev6.github.com/MiniParse

# MiniParse is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# MiniParse is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with MiniParse.  If not, see <http://www.gnu.org/licenses/>.

from Syntax import Syntax
from Rule import Rule
from Alternative import Alternative
from Sequence import Sequence
from Repetition import Repetition
from Terminal import Terminal
from NonTerminal import NonTerminal
from Null import Null


class Builder:
    def makeSyntax(self, rules):  # pragma no cover
        return Syntax(rules)

    def makeRule(self, name, d):  # pragma no cover
        return Rule(name, d)

    def makeAlternative(self, elems):  # pragma no cover
        return Alternative(elems)

    def makeSequence(self, elems):  # pragma no cover
        return Sequence(elems)

    def makeRepeated(self, x):  # pragma no cover
        return Repetition(Null, x)

    def makeOptional(self, x):  # pragma no cover
        return Alternative([Null, x])

    def makeTerminal(self, value):  # pragma no cover
        return Terminal(value)

    def makeNonTerminal(self, value):  # pragma no cover
        return NonTerminal(value)
