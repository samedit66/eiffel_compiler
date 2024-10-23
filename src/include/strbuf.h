#ifndef __STRBUF_H__
#define __STRBUF_H__

/**
 * Строковый буффер.
 * Используется для аккумулирования строк.
 */
typedef struct StringBuffer {
    /**
     * Указатель на "сырой" буффер в виде zero-terminated строки
     */
    char *buffer;

    /**
     * Текущий размер строки (эквивалентен strlen(buffer))
     */
    int size;
    
    /**
     * Емкость строки
     */
    int cap;
} StringBuffer;

/**
 * Конструктор создания строкового буффера из zero-terminated строки
 * 
 * @param  cstr строка, оканчивающаяся символом '\0'
 * @return строковый буффер с начальным значением в виде переданной строки, либо NULL,
 * если не получилось выделить память для буффера
 */
StringBuffer*
StringBuffer_new(char *cstr);

/** 
 * Конструктор создания пустого строкового буффера
 * 
 * @return пустой строковый буффер
 */
StringBuffer*
StringBuffer_empty();

/**
 * Добавляет zero-terminated строку в конец буффера
 * 
 * @param strbuf строковый буффер
 * @param cstr   строка, оканчивающаяся символом '\0'
 */
StringBuffer*
StringBuffer_append(StringBuffer *strbuf, char *cstr);

/**
 * Добавляет символ в конец буффера
 * 
 * @param strbuf строковый буффер
 * @param ch     символ
 */
StringBuffer*
StringBuffer_append_char(StringBuffer *strbuf, char ch);

/**
 * Очищает содержимое буффера
 * 
 * @param strbuf строковый буффер
 */
void
StringBuffer_clear(StringBuffer *strbuf);

/**
 * Освобождает память, занятую буффером
 * 
 * @param strbuf строковый буффер
 */
void
StringBuffer_delete(StringBuffer *strbuf);

#endif
