// Stack Implementation
// Author: xxc3nsoredxx

#include <stdlib.h>
#include <stdio.h>
#include "stack.h"

// Initialize a stack
stack_t* init () {
    stack_t *ret = (stack_t*) malloc (sizeof (stack_t));

    ret->top = 0;
    ret->bottom = 0;

    return ret;
}

// Push value onto stack
bool push (stack_t *s, int value) {
    stack_entry_t *temp = (stack_entry_t*) malloc (sizeof (stack_entry_t));
    
    if (s->top == 0) {
        temp->value = value;
        temp->next = 0;
        s->top = temp;
        s->bottom = temp;

        return true;
    }

    temp->value = value;
    temp->next = s->top;
    s->top = temp;

    return true;
}

// Pop value from stack
// Returns 0 if popping an empty stack
int pop (stack_t *s) {
    int ret = s->top->value;
    
    // If the current top of the stack is the only member, reset values
    // Else set the top of the stack to the next one and free the old top
    if (s->top == s->bottom && s->top != 0) {
        s->top->value = 0;
        s->top->next = 0;
    } else if (s->top != 0) {
        stack_entry_t *del = s->top;
        s->top = s->top->next;
        free(del);
    }

    return ret;
}

// Flush the stack
bool clear (stack_t *s) {
    while (s->top->next != 0) {
        pop (s);
    }

    return true;
}
