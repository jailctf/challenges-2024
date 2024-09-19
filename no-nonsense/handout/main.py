#!/usr/local/bin/python3
from ast import parse, NodeVisitor

inp = input('> ')
if any(c in inp for c in '([=])'):
    print('no.')
    exit()

class NoNonsenseVisitor(NodeVisitor):
    def visit_Name(self, n):
        if n.id in inp:  # surely impossible to get around this since all utf8 chars will be the same between ast.parse and inp, right?
            print('no ' + n.id)
            exit()


NoNonsenseVisitor().visit(parse(inp))

exec(inp)  # management told me they need to use exec and not eval. idk why but they said something about multiline statements? idk

