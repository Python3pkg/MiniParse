#!/bin/bash
# -*- coding: utf-8 -*-

# Copyright 2013 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of MiniParse. http://jacquev6.github.com/MiniParse

# MiniParse is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# MiniParse is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with MiniParse.  If not, see <http://www.gnu.org/licenses/>.

function publish {
    check
    test
    bump
    # doc
    push
}

function check {
    pep8 --ignore=E501 . || exit
}

function test2 {
    generate
    coverage2 run --branch --include=MiniParse/*.py --omit=MiniParse/tests/*.py setup.py test --quiet || exit
    coverage2 report --show-missing || exit
}

function test3 {
    python3 setup.py test --quiet || exit
}

function test {
    # test3
    test2
}

function bump {
    previousVersion=$(grep '^version =' setup.py | sed 's/version = \"\(.*\)\"/\1/')
    echo "Next version number? (previous: '$previousVersion')"
    read version
    sed -i -b "s/version = .*/version = \"$version\"/" setup.py
}

function doc {
    rm -rf doc/build
    mkdir doc/build
    cd doc/build
    git init
    sphinx-build -b html -d doctrees .. . || exit
    touch .nojekyll
    echo /doctrees/ > .gitignore
    git add . || exit
    git commit --message "Automatic generation" || exit
    git push --force ../.. HEAD:gh-pages || exit
    cd ../..
}

function push {
    echo "Break (Ctrl+c) here if something is wrong. Else, press enter"
    read foobar

    git commit -am "Publish version $version"

    cp COPYING* MiniParse
    python setup.py sdist upload
    rm -rf MiniParse/COPYING*

    git tag -m "Version $version" $version

    git push github master master:develop
    git push --force github gh-pages
    git push --tags
}

function run2to3 {
    2to3 --write --nobackups MiniParse
}

function generate {
    python -m MiniParse.Meta --in MiniParse/Examples/StringArithmetic/Grammar.ebnf generate --out MiniParse/Examples/StringArithmetic/Parser.py --import ParsingUtilities --match-name-lambda 'lambda n: "ParsingUtilities.make" + n' --main-rule StringExpr
    python -m MiniParse.Meta --in MiniParse/Examples/StringArithmetic/Grammar.ebnf draw
}

$1
