# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

Repetition = "*"
Except = "-"
Concatenate = ","
DefinitionSeparator = "|"
Defining = "="
Terminator = ";"

StartGroup = "("
EndGroup = ")"
StartOption = "["
EndOption = "]"
StartRepeat = "{"
EndRepeat = "}"


class Terminal:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return other.__class__ == Terminal and other.value == self.value

    def __repr__(self):  # pragma no cover
        return "Terminal(" + self.value + ")"


class Comment:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):  # pragma no cover
        return other.__class__ == Comment and other.value == self.value

    def __repr__(self):  # pragma no cover
        return "Comment(" + self.value + ")"


class MetaIdentifier:
    def __init__(self, words):
        self.value = " ".join(words)

    def __eq__(self, other):
        return other.__class__ == MetaIdentifier and other.value == self.value

    def __repr__(self):  # pragma no cover
        return "MetaIdentifier(" + self.value + ")"


class Integer:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return other.__class__ == Integer and other.value == self.value

    def __repr__(self):  # pragma no cover
        return "Integer(" + str(self.value) + ")"
