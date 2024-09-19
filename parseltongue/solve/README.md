# parseltongue

ok i have no clue what the hell we did but it worked and it works so i dont care lol

brief overview:

1) `LOAD_FAST` OOB read to get builtins dict
2) `UNPACK_EX` and `STORE_FAST` to get arb dict keys
3) `MATCH_KEYS` to get arb dict values
4) overwrite the `send` attr of some obj and then get the string with `SWAP` or smth and then call with `SEND` opcode with perl idk wtf is going on but it works

