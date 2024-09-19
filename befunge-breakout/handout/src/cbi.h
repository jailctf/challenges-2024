#ifndef CBI_H_20161011_193425
#define CBI_H_20161011_193425

#include "delta.h"

#define MAKE_PRINT(X) (X) = (((X) < 0x20 || (X) > 0x7E) ? 0x20 : (X))
#define NUM(X) (((X) <= 0x39) ? (X) - 0x30 : 10 + (X) - 0x61)
#define ABS(X) (((X) < 0) ? (-(X)) : (X))

typedef enum ascii_mode_e {
    OFF, SINGLE, MULTI
} ascii_mode_t;

typedef struct instruction_space_t {
    int num_rows;
    int num_cols;
    char **space;
} instruction_space;

void (*direction[4]) (delta_t*) = {up, down, left, right};

#endif
