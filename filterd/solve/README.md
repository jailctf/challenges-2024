# filter'd

### intended solution

ok so basically the solve idea is we can call the function f, and since the eval is called with the globals() as the second argument, we can also set/overwrite variables in the global scope

one important thing to know is that one can delimit statements with `;` instead of `\n` in python

so we can do `f(input())` to regain execution with 4 bytes to spare, but that is not enough to do anything meaningful

instead, we can do `i=input;f(i())` which does the same thing. this may seem not useful to do it this way, because we use more bytes, but that means that
in the "next time through" we can do `f(i())` to run the program again, which is only 6 bytes. that way, we have 8 bytes to spare (well, 7 because one is going to be a `;`).

with the 7 bytes, we can overwrite the `M` to raise the limit to be large

so, `M=10000;f(i())` is our next step

after that, we can just write in whatever payload that doesnt use the blacklisted keywords that we can think of. an easy way to win is just to use the `"os.system"` with `"sh"` as the argument to get a shell and then win

summary of intended sol:
```
i=input;f(i())
M=10000;f(i())
__import__('os').system('sh')
```

### alternative solution

alt sol found by lyndon using walrus operator that uses 13 bytes per inp max

```
f(i:=input())
f(input())
M=10000;f(i)
import os;os.system('sh')
```

i did not make the challenge 13 bytes max because this is an introductory challenge and this would be stretching it a little too far (even i did not see this one coming)

