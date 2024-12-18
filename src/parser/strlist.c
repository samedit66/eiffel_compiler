#include <stdlib.h>
#include <string.h>

#include "./include/strlist.h"
#include "./include/strbuf.h"

static Node*
Node_new(char *value) {
    Node *new_node = (Node*) malloc(sizeof(Node));
    if (new_node == NULL)
        return NULL;

    new_node->value = value;
    new_node->next = NULL;

    return new_node;
}

StringList*
StringList_new() {
    StringList *strlist = (StringList*) malloc(sizeof(StringList));
    strlist->first = strlist->last = NULL;
    return strlist;
}

StringList*
StringList_push(StringList *strlist, const char *str) {
    char *str_copy = strdup(str);
    if (str_copy == NULL)
        return NULL;

    Node *new_last = Node_new(str_copy);
    if (new_last == NULL)
        return NULL;

    if (strlist->first == NULL && strlist->last == NULL) {
        strlist->first = new_last;
        strlist->last = strlist->first;
    }
    else if (strlist->first == strlist->last) {
        strlist->last = new_last;
        strlist->first->next = strlist->last;
    }
    else {
        strlist->last->next = new_last;
        strlist->last = new_last;
    }

    return strlist;
}

int
StringList_size(const StringList *strlist) {
    int size = 0;

    Node *current = strlist->first;
    while (current != NULL) {
        current = current->next;
        size++;
    }

    return size;
}

char*
StringList_get(const StringList *strlist, int index) {
    int elements_count = StringList_size(strlist);
    if (index >= elements_count)
        return NULL;

    Node *needed = strlist->first;

    while (index > 0) {
        needed = needed->next;
        index--;
    }

    return needed->value;
}

char*
StringList_join(const StringList *strlist, const char *delim) {
    StringBuffer *strbuf = StringBuffer_empty();
    if (strbuf == NULL)
        return NULL;

    int list_size = StringList_size(strlist);
    for (int i = 0; i < list_size; i++) {
        void *result = StringBuffer_append(strbuf, StringList_get(strlist, i));
        if (result == NULL) {
            StringBuffer_delete(strbuf);
            return NULL;
        }
        
        if (i != list_size - 1) 
            StringBuffer_append(strbuf, delim);
    }

    char *raw_buffer = strdup(strbuf->buffer);
    if (raw_buffer == NULL)
        return NULL;

    StringBuffer_delete(strbuf);
    return raw_buffer;
}

void
StringList_clear(StringList *strlist) {
    Node *current = strlist->first;

    while (current != NULL) {
        free(current->value);
        Node *temp = current->next;
        free(current);
        current = temp;
    }

    strlist->first = strlist->last = NULL;
}

void
StringList_delete(StringList *strlist) {
    StringList_clear(strlist);
    free(strlist);
}
