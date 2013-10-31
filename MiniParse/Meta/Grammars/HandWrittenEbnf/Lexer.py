# -*- coding: utf-8 -*-

# Copyright 2013 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of MiniParse. http://jacquev6.github.com/MiniParse

# MiniParse is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# MiniParse is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with MiniParse.  If not, see <http://www.gnu.org/licenses/>.

import re

import Tokens as Tok


class Lexer:
    def __init__(self):
        self.__space = re.compile("[ \t\n\r\v\f]*")
        self.__terminal1 = re.compile('".*?"')
        self.__terminal2 = re.compile("'.*?'")
        self.__comment = re.compile("\(\*.*?\*\)", re.DOTALL)
        self.__metaIdentifierWord = re.compile("[a-zA-Z][a-zA-Z0-9]*")
        self.__integer = re.compile("[0-9]+")
        self.__operators = {
            "*": Tok.Repetition,
            "-": Tok.Except,
            ",": Tok.Concatenate,
            "|": Tok.DefinitionSeparator,
            "=": Tok.Defining,
            ";": Tok.Terminator,

            "(": Tok.StartGroup,
            ")": Tok.EndGroup,
            "[": Tok.StartOption,
            "]": Tok.EndOption,
            "{": Tok.StartRepeat,
            "}": Tok.EndRepeat
        }

    def __call__(self, s):
        return list(self.__run(s))

    def __run(self, s):
        i = self.__skipSpaces(s, 0)
        while i < len(s):
            i, tok = self.__next(s, i)
            if not isinstance(tok, Tok.Comment):
                yield tok

    def __skipSpaces(self, s, i):
        return self.__space.match(s, i).end()

    def __next(self, s, i):
        m = self.__integer.match(s, i)
        if m:
            return self.__skipSpaces(s, m.end()), Tok.Integer(int(m.group()))
        m = self.__terminal1.match(s, i)
        if m:
            return self.__skipSpaces(s, m.end()), Tok.Terminal(m.group()[1:-1])
        m = self.__terminal2.match(s, i)
        if m:
            return self.__skipSpaces(s, m.end()), Tok.Terminal(m.group()[1:-1])
        m = self.__comment.match(s, i)
        if m:
            return self.__skipSpaces(s, m.end()), Tok.Comment(m.group()[2:-2].strip())
        if s[i:i + 2] == "(*":
            raise Exception(s[i:], i)
        m = self.__metaIdentifierWord.match(s, i)
        if m:
            words = []
            while m:
                i = m.end()
                words.append(m.group())
                i = self.__skipSpaces(s, i)
                m = self.__metaIdentifierWord.match(s, i)
            return self.__skipSpaces(s, i), Tok.MetaIdentifier(words)
        if s[i] in self.__operators:
            return self.__skipSpaces(s, i + 1), self.__operators[s[i]]
        raise Exception(s[i:], i)
