# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

from . import Null


class Repetition:
    def __init__(self, forward, backward):
        self.forward = forward
        self.backward = backward

    def getExtents(self, drawer):
        forwardRight, forwardUp, forwardDown = self.forward.getExtents(drawer)
        backwardRight, backwardUp, backwardDown = self.backward.getExtents(drawer)

        return (
            max(forwardRight, backwardRight) + 2 * drawer.baseLength,
            forwardUp,
            forwardDown + drawer.baseLength + backwardUp + backwardDown
        )

    def draw(self, drawer):
        forwardRight, forwardUp, forwardDown = self.forward.getExtents(drawer)
        backwardRight, backwardUp, backwardDown = self.backward.getExtents(drawer)

        maxNodeDxRight = max(forwardRight, backwardRight)

        turnLeft, turnRight = drawer.getTurns()

        drawer.advance()
        drawer.advance((maxNodeDxRight - forwardRight) / 2)
        self.forward.draw(drawer)
        drawer.advance((maxNodeDxRight - forwardRight) / 2)
        with drawer.branch:
            turnRight()
            drawer.advance(forwardDown + backwardUp)
            turnRight()
            drawer.advance((maxNodeDxRight - backwardRight) / 2)
            self.backward.draw(drawer)
            drawer.advance((maxNodeDxRight - backwardRight) / 2)
            turnRight()
            drawer.advance(forwardDown + backwardUp)
            turnRight()
        drawer.advance()

    def __repr__(self):
        return "Repetition(" + repr(self.forward) + ", " + repr(self.backward) + ")"

    def __eq__(self, other):
        return repr(self) == repr(other)

    def _simplify(self):
        return Repetition(self.forward._simplify(), self.backward._simplify())

    def _getAtomicSuffix(self):
        return self

    def _removeAtomicSuffix(self):
        return Null.Null

    def _getAtomicPrefix(self):
        return self

    def _removeAtomicPrefix(self):
        return Null.Null
