#ifndef _STRBUF_H
#define _STRBUF_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define DEFAULT_BUFFER_CAPACITY 32


typedef struct strbuf {
    char *buffer;
    int size;
    int cap;
} strbuf;


static inline int calculate_capacity(int size) {
    return (size + 1) * 1.75;
}

strbuf* strbuf_new(char* const c_str) {
    int size, cap;
    if (c_str == NULL) {
        size = 0;
        cap = DEFAULT_BUFFER_CAPACITY;
    }
    else {
        size = strlen(c_str);
        cap = calculate_capacity(size);
    }

    char* buffer = (char*) calloc(cap, sizeof(char));
    if (c_str != NULL) {
        strcpy(buffer, c_str);
    }

    strbuf* str = (strbuf*) malloc(sizeof(strbuf));
    str->buffer = buffer;
    str->size = size;
    str->cap = cap;

    return str;
}

strbuf* strbuf_empty(void) {
    return strbuf_new(NULL);
}

void strbuf_append(strbuf* const buf, char* const c_str) {
    int c_str_len = strlen(c_str);

    if (buf->size + c_str_len >= buf->cap) {
        int new_cap = calculate_capacity(buf->size + c_str_len);
        char* new_buffer = (char*) calloc(new_cap, sizeof(char));
        strcpy(new_buffer, buf->buffer);
        
        free(buf->buffer);

        buf->buffer = new_buffer;
        buf->size = strlen(new_buffer);
        buf->cap = new_cap;
    }

    strcpy(buf->buffer + buf->size, c_str);
    buf->size += c_str_len;
}

void strbuf_append_char(strbuf* const buf, char c) {
    char c_str[2];
    sprintf(c_str, "%c", c);
    strbuf_append(buf, c_str);
}

void strbuf_clear(strbuf* const buf) {
    if (buf->size > 0) {
        buf->buffer[0] = '\0';
    }
    buf->size = 0;
}

void strbuf_destroy(strbuf* const buf) {
    free(buf->buffer);
    free(buf);
}

#endif
