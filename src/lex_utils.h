#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>

#include "strbuf.h"

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

// Взято из: https://stackoverflow.com/questions/2725385/standard-c-library-for-escaping-a-string
char* escape(char* ptr) {
    if (!ptr) return NULL;

    strbuf* buf = strbuf_empty();
    int len = strlen(ptr);
    for (int i = 0; i < len; i++, ptr++) {
        switch (*ptr) {
            case '\0': strbuf_append(buf, "\\0");  break;
            case '\a': strbuf_append(buf, "\\a");  break;
            case '\b': strbuf_append(buf, "\\b");  break;
            case '\f': strbuf_append(buf, "\\f");  break;
            case '\n': strbuf_append(buf, "\\n");  break;
            case '\r': strbuf_append(buf, "\\r");  break;
            case '\t': strbuf_append(buf, "\\t");  break;
            case '\v': strbuf_append(buf, "\\v");  break;
            case '\\': strbuf_append(buf, "\\\\"); break;
            case '\?': strbuf_append(buf, "\\\?"); break;
            case '\'': strbuf_append(buf, "\\\'"); break;
            case '\"': strbuf_append(buf, "\\\""); break;
            default:
                if (isprint(*ptr)) {
                    strbuf_append_char(buf, *ptr);
                }
                else {
                    // Потенциально способно вызвать segfault, в силу того
                    // что добавление символов идет в обход любого append...
                    int size = sprintf(buf->buffer, "\\%03o", *ptr);
                    buf->size += size;
                }
        }
    }

    char* copy = strdup(buf->buffer);
    strbuf_destroy(buf);
    return copy;
}
    