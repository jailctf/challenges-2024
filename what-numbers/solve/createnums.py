# warning: uses at least 10gb ram (this can be defo optimized, however)

numbers = {
    1: '__debug__',
    2: 'exit.__call__.__code__.co_nlocals',
    3: 'check.__code__.co_stacksize',
    4: 'int.__itemsize__',
    5: 'credits.__call__.__code__.co_nlocals',
    6: 'exit.__call__.__code__.co_stacksize',
    8: 'tuple.__itemsize__',
    9: '__loader__.set_data.__code__.co_nlocals',
    10: '__loader__.get_source.__code__.co_stacksize',
    11: '__loader__.set_data.__code__.co_stacksize',
    14: 'exit.__init__.__code__.co_firstlineno',
    15: '__loader__.get_code.__code__.co_nlocals',
    16: 'object.__basicsize__',
    17: 'exit.__repr__.__code__.co_firstlineno',
    19: 'exit.__call__.__code__.co_firstlineno',
    24: 'int.__basicsize__',
    31: '__loader__.load_module.__code__.co_flags',
    32: 'map.__basicsize__',
    33: 'bytes.__basicsize__',
    35: 'credits.__init__.__code__.co_firstlineno',
    40: 'type.__itemsize__',
    48: 'zip.__basicsize__',
    56: 'bytearray.__basicsize__',
    60: 'credits.__repr__.__code__.co_firstlineno',
    64: 'property.__basicsize__',
    67: 'check.__code__.co_flags',
    79: 'help.__call__.__code__.co_flags',
    80: 'str.__basicsize__',
    88: 'check.__class__.__dictoffset__',
    96: 'check.__class__.__weakrefoffset__',
    98: 'help.__repr__.__code__.co_firstlineno',
    101: 'help.__call__.__code__.co_firstlineno',
    128: 'check.__class__.__basicsize__',
    136: 'memoryview.__weakrefoffset__',
    144: 'memoryview.__basicsize__',
    176: 'check.__code__.__class__.__basicsize__',
    192: 'set.__weakrefoffset__',
    200: 'set.__basicsize__',
    264: 'type.__dictoffset__',
    368: 'type.__weakrefoffset__',
    542: '__loader__.load_module.__code__.co_firstlineno',
    866: '__loader__.is_package.__code__.co_firstlineno',
    874: '__loader__.create_module.__code__.co_firstlineno',
    877: '__loader__.exec_module.__code__.co_firstlineno',
    888: 'type.__basicsize__',
    893: '__loader__.path_mtime.__code__.co_firstlineno',
    932: '__loader__.get_source.__code__.co_firstlineno',
    942: '__loader__.source_to_code.__code__.co_firstlineno',
    950: '__loader__.get_code.__code__.co_firstlineno',
    1040: '__loader__.__init__.__code__.co_firstlineno',
    1046: '__loader__.__eq__.__code__.co_firstlineno',
    1050: '__loader__.__hash__.__code__.co_firstlineno',
    1070: '__loader__.get_data.__code__.co_firstlineno',
    1089: '__loader__.path_stats.__code__.co_firstlineno',
    1094: '__loader__._cache_bytecode.__code__.co_firstlineno',
    1099: '__loader__.set_data.__code__.co_firstlineno',
    4384: 'range.__flags__',
    5376: 'complex.__flags__',
    20736: 'slice.__flags__',
    20768: 'memoryview.__flags__',
    21760: 'zip.__flags__',
    528640: '....__class__.__flags__',
    529664: 'object.__flags__',
    545088: 'type.__dict__.__class__.__flags__',
    545152: 'int.imag.__class__.__flags__',
    546304: 'exit.__class__.__flags__',
    547072: 'exit.__call__.__class__.__flags__',
    547200: 'id.__class__.__flags__',
    676224: 'int.__eq__.__class__.__flags__',
    678144: 'check.__class__.__flags__',
    678272: 'set.add.__class__.__flags__',
    4199680: 'float.__flags__',
    4740352: 'set.__flags__',
    21500160: 'bool.__flags__',
    21501184: 'int.__flags__',
    38294816: 'list.__flags__',
    71849248: 'tuple.__flags__',
    138941696: 'bytes.__flags__',
    273159424: 'str.__flags__',
    541611328: 'dict.__flags__',
    2148031744: 'type.__flags__',
}
numbers_keys = list(numbers.keys())
for k_ in numbers_keys:
    numbers[-k_] = "-" + numbers[k_]
numbers_keys = list(numbers.keys())
bound = 2 ** 400
max_code_len = 75  # only applies after addsub and muldiv steps


def main(goals: list[int]):
    """
    in terms of operator precedence, negation happens first,
    mul+dev happens next, then add+sub happens next, and finally, xor
    """
    # mul+div happens first (actually negation does but whatever)
    after_muldiv = {}
    # setup
    for k in numbers:
        after_muldiv[k] = numbers[k]
    # add multiplication results
    for ai in range(len(numbers)):
        for bi in range(ai+1, len(numbers)):
            eq = numbers[numbers_keys[ai]] + "*" + numbers[numbers_keys[bi]]
            res = numbers_keys[ai]*numbers_keys[bi]
            if -bound < res < bound:
                if res not in after_muldiv or len(after_muldiv[res]) > len(eq):
                    after_muldiv[res] = eq
    print("done mul")
    # add floor division results
    for a in numbers:
        for b in numbers:
            if a == b:
                continue
            eq = numbers[a] + "//" + numbers[b]
            if b == 0:
                continue
            res = a//b
            if -bound < res < bound:
                if res not in after_muldiv or len(after_muldiv[res]) > len(eq):
                    after_muldiv[res] = eq
    print("done floordiv")
    # filter by length
    first = {}
    for k in sorted(after_muldiv):
        if len(after_muldiv[k]) <= max_code_len:
            first[k] = after_muldiv[k]
    first_keys = list(first.keys())

    # then add and minus
    after_addsub = {}
    # setup
    for k in first:
        after_addsub[k] = first[k]
    # add addition results
    for ai in range(len(first)):
        for bi in range(ai+1, len(first)):
            if first[first_keys[bi]][0] == "-":
                eq = first[first_keys[ai]] + first[first_keys[bi]]
            else:
                eq = first[first_keys[ai]] + "--" + first[first_keys[bi]]
            res = first_keys[ai]--first_keys[bi]
            if -bound < res < bound:
                if res not in after_addsub or len(after_addsub[res]) > len(eq):
                    after_addsub[res] = eq
    print("done addition")
    # add subtraction results
    for a in first:
        for b in first:
            if a == b:
                continue
            eq = first[a] + "-" + first[b]
            res = a-b
            if -bound < res < bound:
                if res not in after_addsub or len(after_addsub[res]) > len(eq):
                    after_addsub[res] = eq
    print("done subtraction")
    # filter by length
    second = {}
    for k in sorted(after_addsub):
        if len(after_addsub[k]) <= max_code_len:
            second[k] = after_addsub[k]
    print("now doing xor goal search")
    for goal in goals:
        print("=" * 50, goal)
        minimum = 9999
        if goal in second:
            print(len(second[goal]), "\t", goal, second[goal])
        for k in second:
            if k ^ goal in second:
                new_len = len(second[k])+len(second[k ^ goal])+1
                if new_len < minimum:
                    minimum = new_len
                    print(new_len, "\t", k, k ^ goal, second[k] + "^" + second[k ^ goal])


if __name__ == '__main__':
    main([419, 420, 421])  # put nums here. i suggest num-1, num, num+1 (adding all three)
