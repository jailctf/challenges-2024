#!/usr/local/bin/python3
from RestrictedPython import compile_restricted
from RestrictedPython import safe_globals, utility_builtins
exec_globals = {**safe_globals, **utility_builtins}
exec_locals = {}
code = input('code > ')
code = compile_restricted(code, '<string>', 'exec')
exec(code, exec_globals, exec_locals)