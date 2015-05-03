# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>


class Syntax:
    def __init__(self, rules):
        self.rules = rules

    def getExtents(self, ctx):
        width = 0
        height = 0

        for rule in self.rules:
            w, h = rule.getExtents(ctx)
            width = max(w, width)
            height += 10 + h
        height -= 10

        return width, height

    def draw(self, ctx):
        for rule in self.rules:
            w, h = rule.getExtents(ctx)
            rule.draw(ctx)
            ctx.translate(0, h + 10)
