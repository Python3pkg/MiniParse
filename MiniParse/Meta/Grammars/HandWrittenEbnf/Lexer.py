# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

import re

import MiniParse
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
            i_before = i
            i, tok = self.__next(s, i)
            if not isinstance(tok, Tok.Comment):
                yield i_before, tok

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
            raise MiniParse.ParsingError("Unclosed comment", i, set())
        if s[i] in ["'", '"']:
            raise MiniParse.ParsingError("Unclosed string", i, set())
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
        raise MiniParse.ParsingError("Unexpected character", i, set())
