#!/usr/bin/env python

import unittest


# EBNF Grammar
# stringExpr = stringTerm, { '+', stringTerm };
# stringTerm = [ ( intTerm | '(', intExpr, ')' ), '*' ], string;
# intExpr = intTerm, { ( '+' | '-' ) , intTerm };
# intTerm = { intFactor, ( '*' | '/' ) }, intFactor;
# intFactor = int | '(', intExpr, ')';
# int = [ '-' ], digit, { digit };
# digit = '0' | '1' | '...' | '9';
# string = '"', { char | escape }, '"';
# escape = '\"';


if __name__ == "__main__":
	unittest.main()
