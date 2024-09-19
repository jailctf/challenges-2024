#!/usr/local/bin/python3
from random import randint


def run_prog(state: str, prog: str):
    steps = 0
    assert " " not in state
    before_outer = None
    splitted = prog.splitlines(keepends=False)
    assert len(splitted) < 200, "too long code"
    while True:
        if before_outer == state:
            break
        before_outer = state
        for line in splitted:
            if len(line.strip()) == 0:
                continue
            statement = line.split(" ")
            if len(statement) == 1:
                if statement[0] == "@":
                    if before_outer != state:
                        break
            else:
                before = None
                while True:
                    if before == state:
                        break
                    before = state
                    state = state.replace(statement[0], statement[1])
                    steps += 1
                    assert steps < 10000, "too many steps"
                    assert len(state) < 4000, "too many state"
    return state


def check_xor(prog: str):
    for _ in range(60):
        a, b = randint(1, 1000), randint(1, 1000)
        if str(a ^ b) != run_prog(f"{a}^{b}", prog):
            return False
    return True


def input_multiline() -> str:
    total = ""
    while (line := input("> ")) != "<END>":
        total += line + '\n'
    return total


def main():
    while True:
        choice = input("do you want to substitute? (y/n) > ")
        if choice.lower()[0] == "y":
            print("input prog, type <END> on a line by itself to stop inputting")
            prog = input_multiline()
            if not check_xor(prog):
                print("incorrect")
                continue
            with open("flag.txt") as f:
                left, *chars = f.read().encode()
                for right in chars:
                    left = int(run_prog(f"{left}^{right}", prog))
            print("xor'd flag bytes:", left)
        else:
            break
    print('bye')


if __name__ == '__main__':
    main()
