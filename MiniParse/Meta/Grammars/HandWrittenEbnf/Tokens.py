# -*- coding: utf-8 -*-

# Copyright 2013 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of MiniParse. http://jacquev6.github.com/MiniParse

# MiniParse is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# MiniParse is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with MiniParse.  If not, see <http://www.gnu.org/licenses/>.

Repetition = "*"
Except = "-"
Concatenate = ","
DefinitionSeparator = "|"
Defining = "="
Terminator = ";"

StartGroup = "("
EndGroup = ")"
StartOption = "["
EndOption = "]"
StartRepeat = "{"
EndRepeat = "}"


class Terminal:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return other.__class__ == Terminal and other.value == self.value

    def __repr__(self):  # pragma no cover
        return "Terminal(" + self.value + ")"


class Comment:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):  # pragma no cover
        return other.__class__ == Comment and other.value == self.value

    def __repr__(self):  # pragma no cover
        return "Comment(" + self.value + ")"


class MetaIdentifier:
    def __init__(self, words):
        self.value = " ".join(words)

    def __eq__(self, other):
        return other.__class__ == MetaIdentifier and other.value == self.value

    def __repr__(self):  # pragma no cover
        return "MetaIdentifier(" + self.value + ")"


class Integer:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return other.__class__ == Integer and other.value == self.value

    def __repr__(self):  # pragma no cover
        return "Integer(" + str(self.value) + ")"
