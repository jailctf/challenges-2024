#!/usr/local/bin/python3
from random import random, seed
from ast import literal_eval


def main():
    a, b = input('> ').split(" ")
    if len(b) > 3346:
        print('nuh uh')
        exit()
    seed(literal_eval(b))
    total_prog = "".join([("".join(map(chr, range(32, 127))) + '\n')[int(random() * 96)] for i in range(literal_eval(a))])
    eval(total_prog)


if __name__ == "__main__":
    main()

