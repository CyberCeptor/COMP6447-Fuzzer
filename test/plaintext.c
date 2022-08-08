// Test that the fuzzer can crash a plaintext input program.

#include <stdio.h>
#include <ctype.h>

#define n "nay "
#define y "yay "

char *translate[] =
{
    n, y, n, y, n, y, n, y, n, y, n, y, n,
    y, n, y, n, y, n, y, n, y, n, y, n, y
};

int main(void)
{
    char buf[32] = {};
    setbuf(stdout, NULL);
    printf("Type something: ");
    fgets(buf, 32, stdin);
    printf("So you like %s", buf);
    for (char *c = buf; *c != '\0'; c++)
    {
        if (isspace(*c)) continue;
        char x = tolower(*c);
        fputs(translate[x - 'a'], stdout);
    }
    putchar('\n');

    return 0;
}
