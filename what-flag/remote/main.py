#!/usr/local/bin/python3
import signal
from time import sleep
from random import random, getrandbits

flag = open('flag.txt').read()
def die(*args):
    raise SystemError

LENGTH_LIMIT = 22 # pretty sure you can't do anything sus with this.
q = input("do whatever: ")[:LENGTH_LIMIT]
r = input("do whateverer: ")[:LENGTH_LIMIT]

signal.signal(signal.SIGALRM, die)
signal.setitimer(signal.ITIMER_REAL, 0.001)

try:
    eval(q, {'__builtins__':{}, "flag":flag}, {'__builtins__':{}, "flag":flag})
except:
    pass

try:
    sleep(0.002)
except:
    pass
del flag
safe_builtins = {i:__builtins__.__dict__[i] for i in __builtins__.__dict__ if type(__builtins__.__dict__[i]) == type} # types are safe right?
sleep(random()) # no side channels :D

try:
    eval(r, {'__builtins__': safe_builtins}, {'__builtins__': safe_builtins})
except:
    pass
