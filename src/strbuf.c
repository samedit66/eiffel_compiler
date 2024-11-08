#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#include "./include/strbuf.h"

static const int DEFAULT_BUFFER_CAPACITY = 32;

static inline int calculate_capacity(int size) {
    return (size + 1) * 1.75;
}

StringBuffer*
StringBuffer_new(const char *cstr) {
    int size, cap;
    char *buffer;

    if (cstr == NULL) {
        size = 0;
        cap = DEFAULT_BUFFER_CAPACITY;
        buffer = calloc(cap, sizeof(char));
    }
    else {
        size = strlen(cstr);
        cap = calculate_capacity(size);
        buffer = calloc(cap, sizeof(char));
        strcpy(buffer, cstr);

        if (buffer == NULL) return NULL;
    }

    StringBuffer* strbuf = (StringBuffer*) malloc(sizeof(StringBuffer));
    strbuf->buffer = buffer;
    strbuf->size = size;
    strbuf->cap = cap;

    return strbuf;
}

StringBuffer*
StringBuffer_empty() {
    return StringBuffer_new(NULL);
}

StringBuffer*
StringBuffer_append(StringBuffer *strbuf, const char *cstr) {
    int cstr_len = strlen(cstr);

    if (strbuf->size + cstr_len >= strbuf->cap) {
        int new_cap = calculate_capacity(strbuf->size + cstr_len);
        char* new_buffer = (char*) calloc(new_cap, sizeof(char));

        if (new_buffer == NULL) return NULL;

        strcpy(new_buffer, strbuf->buffer);
        free(strbuf->buffer);

        strbuf->buffer = new_buffer;
        strbuf->size = strlen(new_buffer);
        strbuf->cap = new_cap;
    }

    strcpy(strbuf->buffer + strbuf->size, cstr);
    strbuf->size += cstr_len;

    return strbuf;
}

StringBuffer*
StringBuffer_append_char(StringBuffer* strbuf, char ch) {
    char cstr[2];
    sprintf(cstr, "%c", ch);
    return StringBuffer_append(strbuf, cstr);
}

void
StringBuffer_clear(StringBuffer *strbuf) {
    if (strbuf->size > 0) {
        strbuf->buffer[0] = '\0';
    }
    strbuf->size = 0;
}

void
StringBuffer_delete(StringBuffer *strbuf) {
    free(strbuf->buffer);
    free(strbuf);
}
