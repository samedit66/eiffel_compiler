#ifndef __JSON_H__
#define __JSON_H__

#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <stdio.h>

#include "strbuf.h"

/**
 * Тип значения поля
 */
typedef enum JsonValueType {
    JSON_STRING,
    JSON_INT,
    JSON_DOUBLE,
    JSON_BOOL,
    JSON_NULL,
    JSON_OBJECT,
    JSON_ARRAY
} JsonValueType;

struct Json;

/**
 * Поле объекта или элемент массива
 */
typedef struct Field {
    /**
     * Тип значения
     */
    JsonValueType value_type;

    /**
     * Имя поля. Может быть NULL, если это элемент массива
     */
    char *field_name;

    /**
     * Само значение
     */
    union {
        char *str_value;
        int int_value;
        double double_value;
        bool bool_value;
        struct Json *object_or_array;
    };

    /**
     * Указатель на следующее поле или элемент массива
     */
    struct Field *next_field;
} Field;

/**
 * JSON-объект или массив
 */
typedef struct Json {
    Field *first;
    Field *last;
} Json;

/**
 * Создает JSON-объекта или массива
 * 
 * @return JSON-объект или массив
 */
Json*
Json_new();

/**
 * Добавляет поле-строку в JSON-объект
 * 
 * @param object     указатель на объект
 * @param field_name имя поля
 * @param value      значение для поля (строка)
 * 
 * @return указатель на тот же объект
 */
Json*
Json_add_string_to_object(Json *object, char *field_name, char *value);

/**
 * Добавляет поле-число с плавающей точкой в JSON-объект
 * 
 * @param object     объект
 * @param field_name имя поля
 * @param value      значение для поля (число с плавающей точкой)
 * 
 * @return указатель на тот же объект
 */
Json*
Json_add_double_to_object(Json *object, char *field_name, double value);

/**
 * Добавляет поле-целое число в JSON-объект
 * 
 * @param object     объект
 * @param field_name имя поля
 * @param value      значение для поля (целое число)
 * 
 * @return указатель на тот же объект
 */
Json*
Json_add_int_to_object(Json *object, char *field_name, int value);

/**
 * Добавляет поле-объект в JSON-объект
 * 
 * @param object       объект
 * @param field_name   имя поля
 * @param object_value значение для поля (указатель на JSON-объект)
 * 
 * @return указатель на тот же объект
 */
Json*
Json_add_object_to_object(Json *object, char *field_name, Json *object_value);

/**
 * Добавляет поле-массив в JSON-объект
 * 
 * @param object     объект
 * @param field_name имя поля
 * @param array      значение для поля (указатель на JSON-массив)
 * 
 * @return указатель на тот же объект
 */
Json*
Json_add_array_to_object(Json *object, char *field_name, Json *array);

/**
 * Добавляет булевское поле в JSON-объект
 * 
 * @param object     объект
 * @param field_name имя поля
 * @param array      значение для поля (булевское значение)
 * 
 * @return указатель на тот же объект
 */
Json*
Json_add_bool_to_object(Json *object, char *field_name, bool value);

/**
 * Добавляет нулевое поле в JSON-объект
 * 
 * @param object     объект
 * @param field_name имя поля
 * 
 * @return указатель на тот же объект
 */
Json*
Json_add_null_to_object(Json *object, char *field_name);

/**
 * Добавляет строковый элемент в JSON-массив
 * 
 * @param array указатель на массив
 * @param value строковое значение
 * 
 * @return указатель на тот же массив
 */
Json*
Json_add_string_to_array(Json *array, char *value);
/**
 * Добавляет число с плавающей точкой в JSON-массив
 * 
 * @param array указатель на массив
 * @param value число с плавающей точкой
 * 
 * @return указатель на тот же массив
 */
Json*
Json_add_double_to_array(Json *array, double value);
/**
 * Добавляет целое число в JSON-массив
 * 
 * @param array указатель на массив
 * @param value целое число
 * 
 * @return указатель на тот же массив
 */
Json*
Json_add_int_to_array(Json *array, int value);

/**
 * Добавляет объект в JSON-массив
 * 
 * @param array  указатель на массив
 * @param object объект
 * 
 * @return указатель на тот же массив
 */
Json*
Json_add_object_to_array(Json *array, Json *object);

/**
 * Добавляет массив в JSON-массив
 * 
 * @param array  указатель на массив
 * @param array_value массив для добавления
 * 
 * @return указатель на массив, в который был добавлен элемент
 */
Json*
Json_add_array_to_array(Json *array, Json *array_value);

/**
 * Добавляет булевское значение в JSON-массив
 * 
 * @param array указатель на массив
 * @param value значение
 * 
 * @return указатель на тот же массив
 */

Json*
Json_add_bool_to_array(Json *array, bool value);
/**
 * Добавляет нулевое значение в JSON-массив
 * 
 * @param array указатель на массив
 * 
 * @return указатель на тот же массив
 */
Json*
Json_add_null_to_array(Json *array);

/**
 * Генерирует JSON-строку для заданного объекта
 * 
 * @param json JSON-объект
 * 
 * @return строка, представляющая данный объект
 */
char*
Json_object_as_string(Json *json);

#endif
