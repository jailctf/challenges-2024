**most files taken from [here](https://github.com/xxc3nsoredxx/c-befunge-int)**

# C Befunge Interpreter

This Befunge interpreter has full support for Befunge-93.

Extra Non-93 Features:
    
* Support for an instruction space of arbitrary size

* Allows pushing hex digits (0-f) as integers

* Allows turning the instruction pointer relative to the current direction

* Allows repeating commands

* Continuous skipping

* Skipping n cells

## Supported Commands

| Command | Description                                                         |
| ------- | ------------------------------------------------------------------- |
| 0...f   | push numerical value                                                |
| +       | pop a, b and push a + b                                             |
| -       | pop a, b and push b - a                                             |
| *       | pop a, b and push a * b                                             |
| /       | pop a, b and push b / a (integer division)                          |
| %       | pop a, b and push b % a (modulus on integers)                       |
| !       | pop a, if a is 0 push 1, else push 0 (logical not)                  |
| `       | pop a, b and push b > a                                             |
| '       | push the next cell as an ascii                                      |
| "       | start string mode, push next cells as ascii up to the next "        |
| .       | pop numerical value from stack and print                            |
| ,       | pop ascii value from stack and print                                |
| :       | duplicate the top of the stack                                      |
| \       | swap the top two values on the stack                                |
| $       | discard the top value on the stack                                  |
| k       | pop n, run next command n + 1 times                                 |
| ^       | set instruction pointer delta to (0, 1)                             |
| v       | set instruction pointer delta to (0, -1)                            |
| <       | set instruction pointer delta to (-1, 0)                            |
| >       | set instruction pointer delta to (1, 0)                             |
| [       | turn the instruction pointer left relative to direction             |
| ]       | turn the instruction pointer right relative to direction            |
| r       | reverses the instruction pointer delta                              |
| ?       | sets the instruction pointer to a random dirction                   |
| _       | horizontal if, pop a, if a = 0, move right, else move left          |
| \|      | vertical if, pop a, if a = 0, move down, else move  up              |
| #       | jumps over the next cell                                            |
| ;       | turns off execution until next ;                                    |
| j       | pop n, jump over the n next cells                                   |
| &       | get an integer from the user and push it                            |
| ~       | get a character from the user and push it                           |
| g       | pop y, x and push the character in the position (x, y), else push 0 |
| p       | pop y, x, a and push the ascii value a into the position (x, y)     |
| @       | halt                                                                |

## Usage

    cbi <befunge source>

## To Compile

To compile "as is" requies gcc. Windows users can use MinGW (tested) or possibly Cygwin (untested). If you use a different compiler than gcc, you can either tweak the makefile or just compile directly from the command line.

### Windows (MinGW32 example, may be slightly different)

    cd src
    mingw32-make win

### Linux

    cd src
    make linux

## Example Programs

| Source File | Description                       |
| ----------- | --------------------------------- |
| calc.bf     | A REPL for Befunge math operators |
| hw.bf       | Hello World                       |

## TODO

Add more example programs. Feel free to submit your own and I will merge them in after testing to make sure they work.
