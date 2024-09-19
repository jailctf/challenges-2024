gcc -Wall -Wextra -std=c99 -c -fno-pie cbi.c
gcc -Wall -Wextra -std=c99 -c -fno-pie delta.c
gcc -Wall -Wextra -std=c99 -c -fno-pie stack.c
gcc -Wall -Wextra -std=c99 -no-pie cbi.o delta.o stack.o -o cbi
