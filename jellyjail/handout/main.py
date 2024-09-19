#!/usr/local/bin/python3
# https://github.com/DennisMitchell/jellylanguage/tree/70c9fd93ab009c05dc396f8cc091f72b212fb188
from jellylanguage.jelly.interpreter import jelly_eval

inp = input()[:2]
banned = "0123456789ỌŒƓVÐ¡"  # good thing i blocked all ways of getting to python eval !!! yep

if not all([c not in inp for c in banned]):
    print('stop using banned')
    exit()

jelly_eval(inp, [])

