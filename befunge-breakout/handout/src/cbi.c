// C Befunge Interpreter
// Author: xxc3nsoredxx

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "cbi.h"
#include "delta.h"
#include "stack.h"

int parse_command (stack_t *stack, delta_t *delta, instruction_space *is, int pos_row, int pos_col) {
    static ascii_mode_t ascii_mode = OFF;
    static int repeat = 1;
    static int skip_num = 0;
    static int toggle_exec = 0;
    static int jumping_back = 0;

    char command = *(*((is->space) + pos_row) + pos_col);

    if (skip_num > 0) {
        skip_num--;
        return 0;
    }

    if (jumping_back) {
        reflect (delta);
        jumping_back = 0;
    }

    if (toggle_exec) {
        if (command == ';') toggle_exec = 0;
        return 0;
    }

    //printf ("%i %i\n", delta->delta_x, delta->delta_y);
    if (ascii_mode == SINGLE) {
        push (stack, (int) command);
        ascii_mode = OFF;
        return 0;
    }

    if (ascii_mode == MULTI) {
        if (command == '\"') {
            ascii_mode = OFF;
            return 0;
        }
        push (stack, (int) command);
        return 0;
    }

    int a = 0;
    for (int cx = 0; cx < repeat; cx++) {
        switch (command) {
            case '0':
            case '1':
            case '2':
            case '3':
            case '4':
            case '5':
            case '6':
            case '7':
            case '8':
            case '9':
            case 'a':
            case 'b':
            case 'c':
            case 'd':
            case 'e':
            case 'f':
                push (stack, NUM(command));
                break;
            case '+':
                a = pop (stack);
                a += pop (stack);
                push (stack, a);
                break;
            case '-':
                a = pop (stack);
                a = -a;
                a += pop (stack);
                push (stack, a);
                break;
            case '*':
                a = pop (stack);
                a *= pop (stack);
                push (stack, a);
                break;
            case '/':
                a = pop (stack);
                if (a == 0) {
                    printf ("Error: division by zero.\n");
                    return 1;
                }
                a = pop (stack) / a;
                push (stack, a);
                break;
            case '%':
                a = pop (stack);
                if (a == 0) {
                    printf ("Error: division by zero.\n");
                    return 1;
                }
                a = pop (stack) % a;
                push (stack, a);
                break;
            case '!':
                a = pop (stack);
                a = (a) ? 0 : 1;
                push (stack, a);
                break;
            case '`':
                a = pop (stack);
                a = (pop (stack) > a) ? 1 : 0;
                push (stack, a);
                break;
            case '\'':
                ascii_mode = SINGLE;
                break;
            case '\"':
                ascii_mode = MULTI;
                break;
            case '.':
                printf ("%i", pop (stack));
                break;
            case ',':
                printf ("%c", (char) pop (stack));
                break;
            case ':':
                a = pop (stack);
                push (stack, a);
                push (stack, a);
                break;
            case '\\':
                {
                    int b = pop (stack);
                    a = pop (stack);
                    push (stack, b);
                    push (stack, a);
                }
                break;
            case '$':
                pop (stack);
                break;
            case 'k':
                repeat = pop (stack);
                repeat += (repeat > 0) ? 1 : 0;
                return 0;
            case '^':
                up (delta);
                break;
            case 'v':
                down (delta);
                break;
            case '<':
                left (delta);
                break;
            case '>':
                right (delta);
                break;
            case '[':
                rel_left (delta);
                break;
            case ']':
                rel_right (delta);
                break;
            case 'r':
                reflect (delta);
                break;
            case '?':
                a = rand () % 4;
                (*(direction + a)) (delta);
                break;
            case '_':
                a = pop (stack);
                if (!a) right (delta);
                else left (delta);
                break;
            case '|':
                a = pop (stack);
                if (!a) down (delta);
                else up (delta);
                break;
            case '#':
                skip_num = 1;
                break;
            case ';':
                toggle_exec = 1;
                break;
            case 'j':
                skip_num = pop (stack);
                if (skip_num < 0) {
                    reflect (delta);
                    skip_num = ABS(skip_num);
                    skip_num -= 2;
                }
                break;
            case '&':
                scanf ("%d", &a);
                push (stack, a);
                break;
            case '~':
                scanf ("%c", (char*) &a);
                push (stack, (char) a);
                break;
            case 'g':
                {
                    a = pop (stack);
                    int x = pop (stack);
                    if (x >= is->num_cols || a >= is->num_rows) push (stack, 0);
                    else push (stack, (char) *(*((is->space) + a) + x));
                }
                break;
            case 'p':
                {
                    int y = pop (stack);
                    int x = pop (stack);
                    a = pop (stack);
                    // If y is out of bounds, extend in the y direction
                    if (y >= is->num_rows) {
                        is->space = (char**) realloc (is->space, sizeof (char*) * (y + 1));
                        for (int i = is->num_rows; i < (y + 1); i++) {
                            *((is->space) + i) = (char*) calloc ((y + 1), 1);
                        }
                        is->num_rows = y + 1;
                    }
                    // If x is out of bounds, extend in the x direction
                    if (x >= is->num_cols) {
                        for (int i = 0; i < is->num_rows; i++) {
                            *((is->space) + i) = (char*) realloc (*((is->space) + i), (x + 1));
                        }
                        is->num_cols = x + 1;
                    }
                    *(*((is->space) + y) + x) = (char) a;
                }
                break;
            case '@':
                return 1;
            default:
                break;
        }
    }

    repeat = 1;

    return 0;
}

int main (int argc, char **argv) {
    setbuf(stdout, 0);
    char *filename; 
    FILE *in;
    // REMOVE--------------------------------
    //int num_rows, num_cols;
    int pos_row, pos_col;
    instruction_space *is;
    char current_read;
    stack_t *stack;
    delta_t delta;
    
    // Seed rand
    time_t t;
    srand ((unsigned) time (&t));

    // Load file
    // File not in args
    if (argc < 2) {
        printf ("Please include a file name\n");
        return -1;
    } else {
        filename = (char*) malloc (strlen (*(argv + 1)));
        filename = *(argv + 1);
    }

    in = fopen (filename, "r");
    // File not found
    if (!in) {
        printf ("File not found: %s\n", filename);
        free (filename);
        return -1;
    }

    // Initialize the instruction space to be a single spot
    is = (instruction_space*) malloc (sizeof (instruction_space));
    is->num_rows = 1;
    is->num_cols = 1;
    is->space = (char**) malloc (sizeof (char*));
    *((is->space) + 0) = (char*) calloc (is->num_cols, 1);
    pos_row = 0;
    pos_col = 0;

    // Each char is read into here
    // Used for testing the char
    current_read = 0;

    // Reads until the end of the file
    while ((current_read = fgetc (in)) != EOF) {
        // If we have a line longer than the previous max, extend them all out one
        if (pos_col == is->num_cols) {
            (is->num_cols)++;
            for (int row = 0; row < is->num_rows; row++) {
                *((is->space) + row) = (char*) realloc (*((is->space) + row), is->num_cols);
                *(*((is->space) + row) + pos_col) = 0x00;
            }
        }

        // Add the instruction into the instruction space
        *(*((is->space) + pos_row) + pos_col) = current_read;
        pos_col++;

        // If there is a newline, add a new row
        if (current_read == '\n') {
            (is->num_rows)++;
            //printf ("%i\n", is->num_rows);
            is->space = (char**) realloc (is->space, sizeof (char*) * is->num_rows);
            *((is->space) + (is->num_rows - 1)) = (char*) calloc (is->num_cols, 1);
            pos_row++;
            pos_col = 0;
        }
    }

    // Make nonprintables whitespace
    for (int r = 0; r < is->num_rows; r++) {
        for (int c = 0; c < is->num_cols; c++) {
            MAKE_PRINT(*(*((is->space) + r) + c));
            //printf ("0x%02X ", *(*((is->space) + r) + c));
        }
        //printf ("\n");
    }

    // Initialize stack
    stack = init ();

    // Set up the delta
    delta.delta_x = 1;
    delta.delta_y = 0;
    pos_row = 0;
    pos_col = 0;

    // Run through instruction space
    while (!(parse_command (stack, &delta, is, pos_row, pos_col))) {
        //printf ("%c\n", *(*((is->space) + pos_row) + pos_col));
        pos_col += delta.delta_x;
        pos_row += delta.delta_y;
        if (pos_col < 0) pos_col = is->num_cols - 1;
        if (pos_col == is->num_cols) pos_col = 0;
        if (pos_row < 0) pos_row = is->num_rows - 1;
        if (pos_row == is->num_rows) pos_row = 0;
    }
    
    // Release everything from memory
    fclose (in);

    // i dont care about memory leaks
    //free (filename);
    //for (int cx = 0; cx < is->num_rows; cx++) {
    //    free (*((is->space) + cx));
    //}
    //free (is->space);
    //free (is);

    //clear (stack);
    //free (stack);

    return 0;
}
