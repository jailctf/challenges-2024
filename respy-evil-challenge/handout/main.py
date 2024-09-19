#!/usr/local/bin/python3
from RestrictedPython import compile_restricted
from RestrictedPython import safe_globals

from RestrictedPython.Guards import full_write_guard
from RestrictedPython.Eval import default_guarded_getiter
safe_globals['_write_'] = full_write_guard
safe_globals['_getiter_'] = default_guarded_getiter

source_code = input("gib code: ")
byte_code = compile_restricted(source_code, '<inline>', 'eval')
eval(byte_code, safe_globals, {})
