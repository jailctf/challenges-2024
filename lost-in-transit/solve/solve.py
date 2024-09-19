from pickle import *

p = bytearray(BINPUT * 256)  # equivalent to a bunch of no-ops
p[1] = ord('C')  # short binbytes
p[0] = 5+78  # eat everything except for the } which creates an empty dict

print(int.from_bytes(p, 'big') + (2**8)**(255+3))  # modified to eat up null bytes which would be interpreted as opcodes
print(11)  # type in 11 for the radiation alert to change \x8b to \x8c (long4 -> short_binunicode)
