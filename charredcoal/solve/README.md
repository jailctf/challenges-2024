# charredcoal

even though we cant abuse those U V or X utf8 chars, we can use the weird s with a circle in the middle which is for some reason ord under 256 even though it is two bytes in utf8

so it says in the docs that the funky "s" is x[y] or smth, but if you look at the source it does getattr !!!! dangerous alert !!!! anyways, we can just use `<<` and `>>` but the singular chars to 
create a lambda or smth idk what it is and then we getattr the globals of it and then the builtins of that and then the breakpoint and for some reason when stuff is printed in the repl, if it is a function it is called
with no args. so we use breakpoint here and then we can just use a standard import os system sh or whatever

```
§§§«»¦__globals__¦builtins¦breakpoint
__import__('os').system('cat flag.txt')
```

yeah my solve is above (one must hex encode it before submitting ! keep that in mind...)

