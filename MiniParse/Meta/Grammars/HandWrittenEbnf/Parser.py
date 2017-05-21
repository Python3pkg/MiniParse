# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

from MiniParse import LiteralParser, SequenceParser, AlternativeParser, OptionalParser, RepeatedParser, parse

from . import Tokens as Tok


class ClassParser:
    def __init__(self, class_, match):
        self.__class = class_
        self.__match = match

    def apply(self, cursor):
        with cursor.backtracking as bt:
            if cursor.finished or not isinstance(cursor.current, self.__class):
                return bt.expected(self.__class.__name__)
            else:
                m = cursor.current
                cursor.advance()
                return bt.success(self.__match(m))


# See http://www.cl.cam.ac.uk/~mgk25/iso-14977.pdf
class Parser:
    def __init__(self, builder):
        assert hasattr(builder, "makeTerminal")
        assert hasattr(builder, "makeNonTerminal")
        assert hasattr(builder, "makeRepeated")
        assert hasattr(builder, "makeOptional")
        assert hasattr(builder, "makeRepetition")
        assert hasattr(builder, "makeRestriction")
        assert hasattr(builder, "makeAlternative")
        assert hasattr(builder, "makeSequence")
        assert hasattr(builder, "makeRule")
        assert hasattr(builder, "makeSyntax")

        class Internal:
            # 4.21
            emptySequence = SequenceParser([], lambda: builder.makeSequence([]))

            # 4.16
            terminal = ClassParser(Tok.Terminal, lambda t: builder.makeTerminal(t.value))

            # 4.14
            metaIdentifier = ClassParser(Tok.MetaIdentifier, lambda name: name.value)
            nonTerminal = ClassParser(Tok.MetaIdentifier, lambda name: builder.makeNonTerminal(name.value))

            # 4.13
            class groupedSequence:
                @staticmethod
                def apply(cursor):
                    return SequenceParser(
                        [
                            LiteralParser(Tok.StartGroup),
                            Internal.definitionsList,
                            LiteralParser(Tok.EndGroup)
                        ],
                        lambda s, d, e: d
                    ).apply(cursor)

            # 4.12
            class repeatedSequence:
                @staticmethod
                def apply(cursor):
                    return SequenceParser(
                        [
                            LiteralParser(Tok.StartRepeat),
                            Internal.definitionsList,
                            LiteralParser(Tok.EndRepeat)
                        ],
                        lambda s, d, e: builder.makeRepeated(d)
                    ).apply(cursor)

            # 4.11
            class optionalSequence:
                @staticmethod
                def apply(cursor):
                    return SequenceParser(
                        [
                            LiteralParser(Tok.StartOption),
                            Internal.definitionsList,
                            LiteralParser(Tok.EndOption)
                        ],
                        lambda s, d, e: builder.makeOptional(d)
                    ).apply(cursor)

            # 4.10
            syntacticPrimary = AlternativeParser(
                [
                    optionalSequence,
                    repeatedSequence,
                    groupedSequence,
                    nonTerminal,
                    terminal,
                    # specialSequence,  # @todo Implement
                    emptySequence
                ]
            )

            # 4.9
            integer = ClassParser(Tok.Integer, lambda i: i.value)

            # 4.8
            syntacticFactor = AlternativeParser(
                [
                    SequenceParser(
                        [integer, LiteralParser(Tok.Repetition), syntacticPrimary],
                        lambda i, rep, p: builder.makeRepetition(i, p)
                    ),
                    syntacticPrimary
                ]
            )

            # 4.7
            syntacticException = syntacticFactor

            # 4.6 and 4.7
            syntacticTerm = AlternativeParser(
                [
                    SequenceParser(
                        [
                            syntacticFactor,
                            LiteralParser(Tok.Except),
                            syntacticException
                        ],
                        lambda a, e, b: builder.makeRestriction(a, b)
                    ),
                    syntacticFactor
                ]
            )

            # 4.5
            singleDefinition = SequenceParser(
                [
                    syntacticTerm,
                    RepeatedParser(
                        SequenceParser(
                            [LiteralParser(Tok.Concatenate), syntacticTerm],
                            lambda s, d: d
                        )
                    )
                ],
                lambda t1, ts: t1 if len(ts) == 0 else builder.makeSequence([t1] + ts)
            )

            # 4.4
            definitionsList = SequenceParser(
                [
                    singleDefinition,
                    RepeatedParser(
                        SequenceParser(
                            [LiteralParser(Tok.DefinitionSeparator), singleDefinition],
                            lambda s, d: d
                        )
                    )
                ],
                lambda d1, ds: d1 if len(ds) == 0 else builder.makeAlternative([d1] + ds)
            )

            # 4.3
            syntaxRule = SequenceParser(
                [metaIdentifier, LiteralParser(Tok.Defining), definitionsList, LiteralParser(Tok.Terminator)],
                lambda name, defining, value, terminator: builder.makeRule(name, value)
            )

            # 4.2
            syntax = RepeatedParser(syntaxRule, builder.makeSyntax)

        self.internal = Internal

    def __call__(self, tokens):
        return parse(self.internal.syntax, tokens)
