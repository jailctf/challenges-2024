#!/usr/local/bin/python3

from secrets import randbits
from typing import Callable, Iterator, Tuple


class MathJailError(Exception):
    pass


class MathJail:
    title: str
    description: str

    def __init__(self, max_size: int):
        self.max_size = max_size

    def run(self, code: str) -> bool:
        func = self.validate(code)
        for input, output in self.gen_test_cases():
            user_output = func(input)
            if not isinstance(user_output, int) or user_output != output:
                return False
        return True

    def gen_test_cases(self) -> Iterator[Tuple[int, int]]:
        raise NotImplementedError

    def validate(self, code: str) -> Callable[[int], int]:
        if len(code) > self.max_size:
            raise MathJailError(f'Code is too large ({len(code)} > {self.max_size})')

        for c in code:
            if c not in 'n+-*/%()':
                raise MathJailError(f'Illegal character: {c!r}')

        try:
            func = eval(f'lambda n: {code}', {}, {})
        except Exception:
            raise MathJailError(f'Could not compile expression')
        return func

    def __repr__(self):
        return self.description


class IncrementJail(MathJail):
    title = 'Add++'
    description = 'Write an expression that takes a positive integer n, and returns n + 1 (e.g.\n' \
                  'n = 12 should yield 13).\n'

    def gen_test_cases(self):
        for n in range(1, 100):
            output = n + 1
            yield (n, output)

class OnesJail(MathJail):
    title = 'Only 1s'
    description = 'Write an expression that takes a positive integer n, and returns an integer\n' \
                  'with n successive ones (e.g. n = 7 should yield 1111111).\n'

    def gen_test_cases(self):
        for n in range(1, 100):
            output = int('1' * n)
            yield (n, output)


class PrimeJail(MathJail):
    title = 'Prime Time'
    description = 'Write an expression that takes a positive integer n, and returns 1 if n is\n' \
                  'prime, 0 otherwise (e.g. n = 37 should yield 1, but n = 35 should yield 0).\n'

    def gen_test_cases(self):
        for n in range(1, 500):
            output = n >= 2 and all(n % d != 0 for d in range(2, n))
            yield (n, output)


class FibonacciJail(MathJail):
    title = 'Fibonacci'
    description = 'Write an expression that takes a positive integer n, and returns the nth\n' \
                  'Fibonacci number (e.g. n = 1 should yield 0 and n = 7 should yield 8).\n'

    def gen_test_cases(self):
        a, b = 0, 1
        for n in range(1, 100):
            yield (n, a)
            a, b = b, a + b

JAIL_LEVELS = [
    IncrementJail(6),
    OnesJail(50),
    PrimeJail(100),
    FibonacciJail(40),
]

if __name__ == '__main__':
    print('Welcome to the MathJail! Prove to me that you are a true math intellectual, and I will\n'
          'let you go. You may only use the most primitive tools (+, -, *, /, %) to aid in your\n'
          'escape. The only limit is your imagination. Enjoy your stay.\n')

    for i, jail in enumerate(JAIL_LEVELS):
        print(f'Level {i+1}: {jail.title}')
        print('-' * 30)
        print(jail)

        code = input(f'Enter your expression ({jail.max_size} characters max): ')

        try:
            result = jail.run(code)
        except Exception as e:
            print(e)
            exit(1)

        if not result:
            print('You have failed.')
            exit(1)

        if i == len(JAIL_LEVELS) - 1:
            with open('flag.txt', 'r') as f:
                print(f"Noooooo, you have beaten me. OK, here's your reward: {f.read()}")
        else:
            print('Good job! You move on to the next level.\n')