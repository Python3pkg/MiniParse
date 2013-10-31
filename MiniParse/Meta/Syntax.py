# -*- coding: utf-8 -*-

# Copyright 2013 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of MiniParse. http://jacquev6.github.com/MiniParse

# MiniParse is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# MiniParse is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with MiniParse.  If not, see <http://www.gnu.org/licenses/>.

import Generable.Syntax as G


class _deepComparable:
    def __eq__(self, other):
        return other.__class__ is self.__class__ and other.__dict__ == self.__dict__


class Syntax(_deepComparable, G.Syntax):
    def __init__(self, rules):
        G.Syntax.__init__(self, rules)


class Rule(_deepComparable, G.Rule):
    def __init__(self, name, definition):
        G.Rule.__init__(self, name, definition)


class Sequence(_deepComparable, G.Sequence):
    def __init__(self, terms):
        G.Sequence.__init__(self, terms)


class Alternative(_deepComparable, G.Alternative):
    def __init__(self, definitions):
        G.Alternative.__init__(self, definitions)


class Repetition(_deepComparable):
    def __init__(self, number, primary):
        pass


class Optional(_deepComparable, G.Optional):
    def __init__(self, definition):
        G.Optional.__init__(self, definition)


class Repeated(_deepComparable, G.Repeated):
    def __init__(self, definition):
        G.Repeated.__init__(self, definition)


class Terminal(_deepComparable, G.Terminal):
    def __init__(self, value):
        G.Terminal.__init__(self, value)


class NonTerminal(_deepComparable, G.NonTerminal):
    def __init__(self, name):
        G.NonTerminal.__init__(self, name)


class Restriction(_deepComparable, G.Restriction):
    def __init__(self, base, exception):
        G.Restriction.__init__(self, base, exception)
