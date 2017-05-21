# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

from . import Null


class Restriction:
    def __init__(self, base, exception):
        self.base = base
        self.exception = exception

    def getExtents(self, drawer):
        exceptionRight, exceptionUp, exceptionDown = self.exception.getExtents(drawer)
        baseRight, baseUp, baseDown = self.base.getExtents(drawer)

        return (
            max(exceptionRight + drawer.baseLength, baseRight) + 2 * drawer.baseLength,
            exceptionUp,
            exceptionDown + drawer.baseLength + baseUp + baseDown
        )

    def draw(self, drawer):
        exceptionRight, exceptionUp, exceptionDown = self.exception.getExtents(drawer)
        baseRight, baseUp, baseDown = self.base.getExtents(drawer)

        maxNodeDxRight = max(exceptionRight + drawer.baseLength, baseRight)

        turnLeft, turnRight = drawer.getTurns()

        with drawer.branch:
            drawer.advance()
            self.exception.draw(drawer)
            drawer.drawDeadEnd()
        turnRight()
        drawer.advance(exceptionDown + baseUp)
        turnLeft()
        drawer.advance((maxNodeDxRight - baseRight) / 2)
        self.base.draw(drawer)
        drawer.advance((maxNodeDxRight - baseRight) / 2)
        turnLeft()
        drawer.advance(exceptionDown + baseUp)
        turnRight()

    def __repr__(self):
        return "Restriction(" + repr(self.base) + ", " + repr(self.exception) + ")"

    def __eq__(self, other):
        return repr(self) == repr(other)

    def _simplify(self):
        return Restriction(self.base._simplify(), self.exception._simplify())

    def _getAtomicSuffix(self):
        return self

    def _removeAtomicSuffix(self):
        return Null.Null

    def _getAtomicPrefix(self):
        return self

    def _removeAtomicPrefix(self):
        return Null.Null
