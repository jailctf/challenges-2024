# x86fuck

the main idea is to use 0x80 and 0x43 since they allow for the following:

- `43` is `inc ebx`
- `80434343` is `add BYTE PTR [ebx+0x43],0x43`
- `80434380` is `add BYTE PTR [ebx+0x43],0x80`

fortunately, 0x43 is coprime to 256, so it is possible to get [ebx+0x43] to any number with enough of `add BYTE PTR [ebx+0x43],0x43`

additionally, adding 0x80 makes it take half as many instructions, on average, to get [ebx+0x43] to any number from 0

the first bit of the code changes ebx to be higher so there is more time to set up shellcode, and the second part actually does the shellcode

solve script in solve.py

