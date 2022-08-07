// Test that the fuzzer can handle json.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "cJSON.h"

char *read_in()
{
    size_t capacity = 32;
    size_t size = 0;
    char *buf = malloc(capacity);

    int curly_num = 0;
    int square_num = 0;
    do
    {
        int c = getchar();
        if (c == EOF) break;
        if (c == '{') curly_num++;
        else if (c == '}') curly_num--;
        else if (c == '[') square_num++;
        else if (c == ']') square_num--;
        buf[size++] = c;
        if (size == capacity)
        {
            capacity *= 2;
            if ((buf = realloc(buf, capacity)) == NULL) exit(0);
        }

    } while (curly_num > 0 || square_num > 0);
    buf[size] = '\0';
    if (size <= 1) exit(0);
    return buf;
}

int main(void)
{
    puts("Welcome to a shoddy json formatter! I own none of the code!");
    puts("Just type away and at the close of the object your json will be printed!");

    char *user = read_in();
    puts(user);
    cJSON *json = cJSON_Parse(user);
    free(user);
    char *out = cJSON_Print(json);
    puts(out);
    free(out);
    cJSON_Delete(json);
    return 0;
}
