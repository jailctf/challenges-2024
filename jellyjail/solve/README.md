# jellyjail

a bunch of chars (`0123456789ỌŒƓVÐ¡`) are all banned

0-9 provide integer literals

that weird O with the dot beneath it is the `chr` function

that OE char allows for a bunch of things, but notably the easy way to `python_eval` a string is banned

the G with the thing on the top right quite literally does `python_eval(input())`, but that is also banned.

the V character is used to do `jelly_eval` which evals a string as jelly code, and that is banned

now taking a look at the D with a line through it and also the upside down exclamation mark. the upside down exclamation mark does ntimes. looking at the source
code for ntimes, we can see instances of `last_input`, and looking at `last_input`, it calls `python_eval(input())`

we can search for what other functions call `last_input`, and there is a function nfind that does it. nfind is used by the `#` character in this, 
so we can just use `#` to get eval of any input

however, there is an error that min arg is an empty sequence. we can just put any value that evaluates to something that is 
not None before, like `⁸`, which pushed `[]` onto the stack (dont ask me how this is not also an empty sequence, because idk what is going on here either).

anyways, then we can just import os , os.system, and then get the flag

