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
    def makeSyntax(self, rules):  # pragma no cover (Too simple)
        return Syntax(rules)

    def makeRule(self, name, d):  # pragma no cover (Too simple)
        return Rule(name, d)

    def makeAlternative(self, elems):  # pragma no cover (Too simple)
        return Alternative(elems)

    def makeSequence(self, elems):
        nodes = []
        for elem in elems:
            if isinstance(elem, Repetition):
                forward = elem.forward
                backward = elem.backward
                while len(nodes) != 0 and self.__isSuffix(nodes[-1], backward):
                    forward = self.__prepend(nodes[-1], forward)
                    backward = self.__removeSuffix(backward)
                    nodes.pop()
                elem = Repetition(forward, backward)
            nodes.append(elem)
        return Sequence(nodes)

    def __isSuffix(self, suffix, node):
        if node.__class__ == suffix.__class__ and node.__dict__ == suffix.__dict__:  # @todo Deep comparison?
            return True
        if isinstance(node, Sequence) and self.__isSuffix(suffix, node.nodes[-1]):
            return True
        return False

    def __prepend(self, prefix, node):
        if node is Null:
            return prefix
        elif isinstance(node, Sequence):
            return Sequence([prefix] + node.nodes)
        else:
            return Sequence([prefix, node])

    def __removeSuffix(self, node):
        if isinstance(node, Sequence):
            if len(node.nodes) == 1:
                return Null
            elif len(node.nodes) == 2:
                return node.nodes[0]
            else:
                return Sequence(node.nodes[:-1])
        else:
            return Null

    def makeRepeated(self, x):  # pragma no cover (Too simple)
        return Repetition(Null, x)

    def makeOptional(self, x):  # pragma no cover (Too simple)
        return Alternative([Null, x])

    def makeTerminal(self, value):  # pragma no cover (Too simple)
        return Terminal(value)

    def makeNonTerminal(self, value):  # pragma no cover (Too simple)
        return NonTerminal(value)
