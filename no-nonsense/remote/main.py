#!/usr/local/bin/python3
from ast import parse, NodeVisitor

inp = input('> ')
if any(c in inp for c in '([=])'):
    print('no.')
    exit()

class NoNonsenseVisitor(NodeVisitor):
    def visit_Name(self, n):
        if n.id in inp:  # surely impossible to get around this since they will be the same between ast.parse and inp, right?
            print('no ' + n.id)
            exit()


NoNonsenseVisitor().visit(parse(inp))

exec(inp)

