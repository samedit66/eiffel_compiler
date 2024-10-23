#ifndef _STRLIST_H
#define _STRLIST_H

#include <stdlib.h>
#include <string.h>
#include <stdio.h>

typedef struct node {
    char *value;
    struct node *next;
} node;

typedef struct strlist {
    node *first;
    node *last;
} strlist;

static node *node_new(char *value) {
    node *new_node = (node*) malloc(sizeof(node));

    new_node->value = value;
    new_node->next = NULL;

    return new_node;
}

strlist *strlist_new() {
    strlist *new_list = (strlist*) malloc(sizeof(strlist));
    new_list->first = new_list->last = NULL;
    return new_list;
}

void strlist_push(strlist *list, const char *str) {
    char *str_copy = strdup(str);

    node *new_last = node_new(str_copy);
    if (list->first == NULL && list->last == NULL) {
        list->first = new_last;
        list->last = list->first;
    }
    else if (list->first == list->last) {
        list->last = new_last;
        list->first->next = list->last;
    }
    else {
        list->last->next = new_last;
        list->last = new_last;
    }
}

int strlist_count(const strlist *list) {
    int count = 0;

    node *current = list->first;
    while (current != NULL) {
        current = current->next;
        count++;
    }

    return count;
}

char *strlist_get(const strlist *list, int index) {
    int elements_count = strlist_count(list);
    if (index >= elements_count)
        return NULL;

    node *needed = list->first;

    while (index > 0) {
        needed = needed->next;
        index--;
    }

    return needed->value;
}

void strlist_clear(strlist *list) {
    node *current = list->first;

    while (current != NULL) {
        free(current->value);
        node *temp = current->next;
        free(current);
        current = temp;
    }

    list->first = list->last = NULL;
}

void strlist_destroy(strlist *list) {
    strlist_clear(list);
    free(list);
}

#endif
