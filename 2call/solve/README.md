# 2call

solve idea is as below

first thing to know is jsfuck

second thing to know is that we can still get arb order of ops using `[expr][+[]]` as equiv to `(expr)`

so with these two, we can determine that the only way to solve this is by making `[]["flat"]["constructor"](str)` which is equal to Function(str)

third thing to know is that we can get the letters for eval and also the strings `btoa`, `atob`, and `console`, and also `(` and `)`.
those functions are built in to node js, so we can just construct an arbitrary string and eval it inside of the other eval

last thing to know is that even though require is undefined for whatever reason, we can use process.mainModule which has the hidden attribute `require`. then, we just spawn a shell and win

