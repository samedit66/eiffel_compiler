#ifndef __STRLIST_H__
#define __STRLIST_H__

#include <stdlib.h>
#include <string.h>

/**
 * Ячейка списка строк
 */
typedef struct Node {
    /**
     * Непосредственное значение - строка
     */
    char *value;

    /**
     * Указатель на следующий элемент в списке
     */
    struct Node *next;
} Node;

/**
 * Список строк
 */
typedef struct StringList {
    /**
     * Указатель на первый символ в списке
     */
    Node *first;

    /**
     * Указатель на последний элемент в списке (используется для оптимизации 
     * времени добавления элемента в конец списка)
     */
    Node *last;
} StringList;

/**
 * Конструктор создания пустого списка
 */
StringList *StringList_new();

/**
 * Добавляет строку в конец списка строк.
 * Переданная строка для добавления копируются.
 * 
 * @param strlist список строк
 * @param str     строка для добавления
 * @return указатель на переданный список строк, либо NULL, если
 * не получилось выделить память для добавления строки
 */
StringList *StringList_push(StringList *strlist, const char *str);

/**
 * Возвращает количество элементов в списке строк
 * 
 * @param strlist список строк
 * @return количество элементов в списке строк
 */
int StringList_size(const StringList *strlist);

/**
 * Возвращает строку из списка по индексу
 * 
 * @param strlist список строк
 * @param index   индекс элемента
 * @return строка по заданному индексу, либо NULL, если передан недопустимый индекс
 */
char *StringList_get(const StringList *strlist, int index);

/**
 * Соединяет строки в списке через заданный разделитель
 * 
 * @param delim разделитель
 * @return соединенные строки через заданный разделитель, либо NULL,
 * если не получилось выделить память под новую строку-результат
 */
char *StringList_join(const StringList *strlist, const char *delim);

/**
 * Очищает список строк
 * 
 * @param strlist список строк
 */
void StringList_clear(StringList *strlist);

/**
 * Освобождает память, занятую списком
 * 
 * @param strlist список строк
 */
void StringList_delete(StringList *strlist);

#endif
