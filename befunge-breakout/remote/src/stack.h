#ifndef STACK_H_20160919_205120
#define STACK_H_20160919_205120

typedef enum bool_e {
    true, false
} bool;

typedef struct stack_entry_s {
    int value;
    struct stack_entry_s *next;
} stack_entry_t;

typedef struct stack_s {
    stack_entry_t *top;
    stack_entry_t *bottom;
} stack_t;

stack_t* init ();
bool push (stack_t*, int);
int pop (stack_t*);
bool clear (stack_t*);

#endif
