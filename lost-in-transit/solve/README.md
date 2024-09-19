# radiation alert

the solve for this one was changing the LONG4 opcode into a SHORT\_BINUNICODE, which would allow us to execute arbitrary pickle code. 
in the python handout, the loaded pickle value is unpacked and there must be two values. we can get the flag by setting up a short binbytes of our own
with the code execution we have and the `}` at the end of the flag to create an empty dict for us to use as the second value, 
then when the two values on the stack are TUPLE2'd, it will be `(<stuff and flag>, {})` which is unpacked and we win

