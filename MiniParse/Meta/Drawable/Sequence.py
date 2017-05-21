# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

from . import Null
from . import Repetition


class Sequence:
    def __init__(self, nodes):
        self.nodes = nodes

    def getExtents(self, drawer):
        right = 0
        up = 0
        down = 0
        for node in self.nodes:
            r, u, d = node.getExtents(drawer)
            right += r
            up = max(up, u)
            down = max(down, d)
        return (right, up, down)

    def draw(self, drawer):
        for node in self.nodes:
            node.draw(drawer)

    def __repr__(self):
        return "Sequence(" + repr(self.nodes) + ")"

    def __eq__(self, other):
        return repr(self) == repr(other)

    def _simplify(self):
        if len(self.nodes) == 0:
            return Null.Null
        elif len(self.nodes) == 1:
            return self.nodes[0]
        else:
            newNodes = []
            for node in self.nodes:
                node = node._simplify()
                if node.__class__ is Sequence:
                    newNodes += node.nodes
                elif node is Null.Null:
                    pass
                elif len(newNodes) != 0 and node.__class__ is Repetition.Repetition and node.backward._getAtomicSuffix() == newNodes[-1]:
                    forward = Sequence([node.backward._getAtomicSuffix(), node.forward])._simplify()
                    backward = node.backward._removeAtomicSuffix()._simplify()
                    newNodes.pop()
                    newNodes.append(Repetition.Repetition(forward, backward))
                elif len(newNodes) != 0 and newNodes[-1].__class__ is Repetition.Repetition and newNodes[-1].backward._getAtomicPrefix() == node:
                    forward = Sequence([newNodes[-1].forward, newNodes[-1].backward._getAtomicPrefix()])._simplify()
                    backward = newNodes[-1].backward._removeAtomicPrefix()._simplify()
                    newNodes.pop()
                    newNodes.append(Repetition.Repetition(forward, backward))
                else:
                    newNodes.append(node)
            return Sequence(newNodes)

    def _getAtomicSuffix(self):
        return self.nodes[-1]._getAtomicSuffix()

    def _removeAtomicSuffix(self):
        return Sequence(self.nodes[:-1] + [self.nodes[-1]._removeAtomicSuffix()])

    def _getAtomicPrefix(self):
        return self.nodes[0]._getAtomicPrefix()

    def _removeAtomicPrefix(self):
        return Sequence([self.nodes[0]._removeAtomicPrefix()] + self.nodes[1:])
