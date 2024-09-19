# what flag?

warning: this is extremely obscure and may invoke nerd emoji in readers

we can abuse the `__flags__` attribute of types to store data

the 19th bit of the `__flags__` attribute gets set on attribute read of a type

```
>>> complex.__flags__
5376
>>> complex.real
<member 'real' of 'complex' objects>
>>> complex.__flags__
529664
```

in this case we can also abuse the fl ligature and then do a side channel on the second input by having the program stall 
if the `complex.__flags__` are too high

general idea is below

```
do whatever: flag[xx]<'x'or 1j.a
do whateverer: 2**complex.__flags__**2
```

that but with the fl ligature instead of "fl" (the xx and 'x' are the inputs)

