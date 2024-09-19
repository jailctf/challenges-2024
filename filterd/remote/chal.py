#!/usr/local/bin/python3
M = 14  # no malicious code could ever be executed since this limit is so low, right?
def f(code):
    assert len(code) <= M
    assert all(ord(c) < 128 for c in code)
    assert all(q not in code for q in ["exec", 
"eval", "breakpoint", "help", "license", "exit"
, "quit"])
    exec(code, globals())
f(input("> "))

