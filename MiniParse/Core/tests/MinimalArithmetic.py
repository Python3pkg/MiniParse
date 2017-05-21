# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest

from MiniParse import OptionalParser, SequenceParser, AlternativeParser, LiteralParser, RepeatedParser

from .Framework import ParserTestCase


class MinimalArithmetic(ParserTestCase):
    def setUp(self):
        ParserTestCase.setUp(self)
        integer = LiteralParser("1")

        class factor:
            @staticmethod
            def apply(c):
                return AlternativeParser([
                    integer,
                    SequenceParser([
                        LiteralParser("("),
                        expr,
                        LiteralParser(")")
                    ])
                ]).apply(c)

        term = SequenceParser([
            factor,
            RepeatedParser(SequenceParser([
                LiteralParser("*"),
                factor
            ]))
        ])

        expr = SequenceParser([
            term,
            RepeatedParser(SequenceParser([
                LiteralParser("+"),
                term
            ]))
        ])

        self.p = expr

    def testComplexSuccess(self):
        self.expectSuccess(
            "1+1*1",
            (  # expr = Seq => tuple
                (  # term = Seq => tuple
                    '1',  # factor = Alt => type of integer => string
                    []  # Rep => list
                ),  # end of term
                [  # Rep => list
                    (  # Seq => tuple
                        '+',  # Lit => string
                        (  # term = Seq => tuple
                            '1',  # factor = Alt => type of integer => string
                            [  # Rep => list
                                (  # Seq => tuple
                                    '*',  # Lit => string
                                    '1'  # factor = Alt => type of integer => string
                                )
                            ]
                        )
                    )
                ]
            )
        )

    def testSimpleSuccess(self):
        self.expectSuccess("1", (('1', []), []))

    def testMediumSuccess_1(self):
        self.expectSuccess("1+1", (('1', []), [('+', ('1', []))]))

    def testMediumSuccess_2(self):
        self.expectSuccess("1*1", (('1', [('*', '1')]), []))

    def testDandlingAdd(self):
        self.expectFailure("1+1+", 4, ["1", "("])

    def testDandlingMult(self):
        self.expectFailure("1*1*", 4, ["1", "("])

    def testUnclosedParenth(self):
        self.expectFailure("1+(1+1", 6, [")", "*", "+"])
