// Test that the fuzzer can crash a csv reader.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int field1;
    float field2;
    char *field3;
} data_row;

data_row table[3] = {};
int row = 0;

void read_marker()
{
    int c = getchar();
    while (c != ',' && c != '\n' && c != EOF)
    {
        c = getchar();
    }
}

void read_field(char *buf)
{
    int c = getchar();
    while (c != ',' && c != '\n' && c != EOF)
    {
        *(buf++) = (char)c;
        c = getchar();
    }
    *buf = '\0';
}

void read_int()
{
    char buf[10];
    read_field(buf);
    table[row].field1 = atoi(buf);
}

void read_float()
{
    char buf[10];
    read_field(buf);
    table[row].field2 = atof(buf);
}

void read_literal()
{
    char buf[20];
    read_field(buf);
    table[row].field3 = strdup(buf);
}

void read_row()
{
    read_int(); read_float(); read_literal();
    row++;
}

void print_row(data_row row)
{
    printf("| %5d | %10f | %-20s |\n", row.field1, row.field2, row.field3);
}

int main(void)
{
    for (int i = 0; i < 3; i++) read_marker();
    for (int i = 0; i < 3; i++) read_row();
    printf("---------------------------------------------\n");
    for (int i = 0; i < 3; i++) print_row(table[i]);
    printf("---------------------------------------------\n");
    return 0;
}
