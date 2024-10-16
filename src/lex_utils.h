#include <stdlib.h>
#include <stdint.h>

void remove_underscores_in_integer(char* str_integer) {
    int i, j;
    i = j = 0;

    while (str_integer[i]) {
        if (str_integer[i] == '_') {
            i++;
            continue;
        }

        str_integer[j++] = str_integer[i++];
    }

    str_integer[j] = '\0';
}

void parse_integer(int64_t* integer, char* str_integer, int base) {
    int offset = 0;
    switch (base) {
        case 2:
        case 8:
        case 16:
            offset = 2;
    }

    remove_underscores_in_integer(str_integer);

    *integer = strtol(str_integer + offset, NULL, base);
}

void parse_real(double* real, char* str_real) {
    *real = strtod(str_real, NULL);
}

char convert_decimal_encoded_char(char *decimal_encoded) {
    return (char) atoi(decimal_encoded + 2);
}

bool isdelim(char c) { 
    static char* delims = " \n\t*/\\-+:;,.()[]{}^<>=";
    return strchr(delims, c) != NULL;
}

bool isoctdigit(char c) {
    return '0' <= c && c <= '7';
}

bool isbindigit(char c) {
    return c == '0' || c == '1';
}
