# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

import sys
import pipes  # For pipes.quote: see http://stackoverflow.com/questions/4748344/whats-the-reverse-of-shlex-split
import InteractiveCommandLine as ICL

from . import Grammars.HandWrittenEbnf
from . import Generable
from . import Drawable


class Generate(ICL.Command):
    def __init__(self, prog):
        ICL.Command.__init__(self, "generate", "Generate a MiniParse parser for the input grammar")
        self.__prog = prog
        self.outputName = None
        self.addOption(ICL.StoringOption("out", "Output file", self, "outputName", ICL.ValueFromOneArgument("NAME")))
        self.computeParserName = lambda n: "".join(w[0].upper() + w[1:] for w in n.split(' ')) + "Parser"
        self.addOption(ICL.StoringOption("parser-name-lambda", "Function to generate the names of parser classes", self, "computeParserName", ICL.ValueFromOneArgument("NAME", eval)))
        self.computeMatchName = lambda n: "lambda x: x"
        self.addOption(ICL.StoringOption("match-name-lambda", "Function to generate the names of 'match' arguments", self, "computeMatchName", ICL.ValueFromOneArgument("NAME", eval)))
        self.imports = []
        self.addOption(ICL.AppendingOption("import", "Module to import in generated code", self.imports, ICL.ValueFromOneArgument("MODULE")))
        self.mainRule = None
        self.addOption(ICL.StoringOption("main-rule", "Main rule of the grammar", self, "mainRule", ICL.ValueFromOneArgument("NAME")))

    def execute(self):
        inputName = self.__prog.inputName
        with open(inputName) as f:
            g = Grammars.HandWrittenEbnf.parse(Generable.builder, f.read())
        if self.outputName is None:
            self.outputName = inputName[:-5] + ".py"
        with open(self.outputName, "w") as f:
            f.write("# This file was generated by MiniParse.Meta. Manual modifications will likely be lost.\n")
            f.write("# Command line:\n#     python -m MiniParse.Meta " + " ".join(pipes.quote(a) for a in sys.argv[1:]) + "\n")
            f.write("\n")
            f.write("import MiniParse\n")
            f.write("\n")
            for i in self.imports:
                f.write("import " + i + "\n")
            f.write("\n")
            f.write("\n")
            f.write(g.generateMiniParser(self.mainRule, self.computeParserName, self.computeMatchName))


class Draw(ICL.Command):
    def __init__(self, prog):
        ICL.Command.__init__(self, "draw", "Draw rail diagram for the input grammar")
        self.__prog = prog
        self.outputName = None
        self.addOption(ICL.StoringOption("out", "Output file", self, "outputName", ICL.ValueFromOneArgument("NAME")))

    def execute(self):
        import cairo

        inputName = self.__prog.inputName
        with open(inputName) as f:
            g = Grammars.HandWrittenEbnf.parse(Drawable.builder, f.read())
        if self.outputName is None:
            self.outputName = inputName[:-5] + ".png"
        img = cairo.ImageSurface(cairo.FORMAT_RGB24, 1, 1)
        ctx = cairo.Context(img)
        ctx.scale(3, 3)
        w, h = g.getExtents(ctx)
        img = cairo.ImageSurface(cairo.FORMAT_RGB24, 3 * int(w) + 10, 3 * int(h) + 10)
        ctx = cairo.Context(img)
        ctx.translate(5, 5)
        ctx.scale(3, 3)
        ctx.set_source_rgb(1, 1, 1)
        ctx.paint()
        ctx.set_source_rgb(0, 0, 0)
        g.draw(ctx)
        img.write_to_png(self.outputName)


class Program(ICL.Program):
    def __init__(self):
        ICL.Program.__init__(self, "python -m MiniParse.Meta")
        self.addOption(ICL.StoringOption("in", "Input file", self, "inputName", ICL.ValueFromOneArgument("NAME")))
        self.addCommand(Generate(self))
        self.addCommand(Draw(self))


Program().execute()
