# -*- coding: utf-8 -*-

# Copyright 2013 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of MiniParse. http://jacquev6.github.com/MiniParse

# MiniParse is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# MiniParse is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with MiniParse.  If not, see <http://www.gnu.org/licenses/>.

import unittest

from MiniParse import OptionalParser, SequenceParser, AlternativeParser, LiteralParser, RepetitionParser

from Framework import ParserTestCase


class MinimalArithmeticTestCase(ParserTestCase):
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
            RepetitionParser(SequenceParser([
                LiteralParser("*"),
                factor
            ]))
        ])

        expr = SequenceParser([
            term,
            RepetitionParser(SequenceParser([
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
