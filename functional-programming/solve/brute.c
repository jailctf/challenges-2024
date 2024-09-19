#include <pthread.h>
#include <stdio.h>
#include <stdint.h>

#define XXPRIME_1 11400714785074694791ULL
#define XXPRIME_2 14029467366897019727ULL
#define XXPRIME_5 2870177450012600261ULL
#define XXPRIME_1_INV 614540362697595703ULL
#define XXPRIME_2_INV 839798700976720815ULL

#define X0 6823068795704846497ULL
#define X1 8932352168822476794ULL

#define TARGET 0x1337133713371337ULL

#define CACHE_DEPTH 28
#define BRUTE_DEPTH 39

static int64_t ntuplehash(uint64_t acc, uint64_t x) {
    acc = acc * XXPRIME_2 + x;
    acc = (acc << 31) | (acc >> 33);
    acc *= XXPRIME_1;
    acc += 2 ^ (XXPRIME_5 ^ 3527539);
    return acc;
}

static int64_t ntuplehash_inv(uint64_t acc, uint64_t x) {
    acc -= 2 ^ (XXPRIME_5 ^ 3527539);
    acc *= XXPRIME_1_INV;
    acc = (acc << 33) | (acc >> 31);
    acc = (acc - x) * XXPRIME_2_INV;
    return acc;
}

#define MSK ((1 << CACHE_DEPTH) - 1)

static uint64_t mitm_cache[MSK + 1];

static void cache_from_start(uint64_t acc, uint64_t state, int depth) {
    if (depth == CACHE_DEPTH) {
        mitm_cache[acc & MSK] = (acc & ~MSK) | state;
        return;
    }
    cache_from_start(ntuplehash(acc, X0), state << 1, depth + 1);
    cache_from_start(ntuplehash(acc, X1), state << 1 | 1, depth + 1);
}

static void brute_from_end(uint64_t acc, uint64_t state, int depth) {
    if (depth == BRUTE_DEPTH) {
        if ((mitm_cache[acc & MSK] & ~MSK) == (acc & ~MSK)) {
            printf("found solution: ");
            uint64_t cached_state = mitm_cache[acc & MSK] & MSK;
            for (uint64_t i = 0; i < CACHE_DEPTH; i++)
                printf("%lu", (cached_state >> (CACHE_DEPTH - i - 1)) & 1);
            for (uint64_t i = 0; i < BRUTE_DEPTH; i++)
                printf("%lu", (state >> i) & 1);
            puts("");
        }
        return;
    }
    brute_from_end(ntuplehash_inv(acc, X0), state << 1, depth + 1);
    brute_from_end(ntuplehash_inv(acc, X1), state << 1 | 1, depth + 1);
}

static void *search(void *arg) {
    uint64_t i = (uint64_t) arg;
    brute_from_end(ntuplehash_inv(ntuplehash_inv(TARGET, i & 2 ? X1 : X0), i & 1 ? X1 : X0), i, 2);
    return NULL;
}

int main() {
    cache_from_start(0, 0, 1);
    cache_from_start(1, 1, 1);

    printf("done caching...\n");

    pthread_t threads[4];
    for (uint64_t i = 0; i < 4; i++)
        pthread_create(&threads[i], NULL, search, (void *)i);
    for (uint64_t i = 0; i < 4; i++)
        pthread_join(threads[i], NULL);
}
