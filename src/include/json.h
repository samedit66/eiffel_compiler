#ifndef __JSON_H__
#define __JSON_H__

#include <stdlib.h>
#include <string.h>

#include "strbuf.h"

/**
 * Тип значения поля
 */
typedef enum JsonValueType {
    JSON_STRING,
    JSON_INT,
    JSON_DOUBLE,
    JSON_OBJECT
} JsonValueType;

struct Json;

/**
 * Поле объекта
 */
typedef struct JsonNode {
    /**
     * Тип значение поля
     */
    JsonValueType value_type;

    /**
     * Имя поля
     */
    char *field_name;

    /**
     * Значение поля
     */
    union {
        char *str_value;
        int int_value;
        double double_value;
        struct Json *object;
    };

    /**
     * Указатель на следующее поле
     */
    struct JsonNode *next_field;
} JsonNode;

/**
 * Представление JSON
 */
typedef struct Json {
    JsonNode *start;
    JsonNode *last;
} Json;

Json *Json_add_string_to_object(Json *json, char *field_name, char *value) {
    JsonNode *prev_field = json->last;

    JsonNode *new_field = (JsonNode *) malloc(sizeof(JsonNode));
    new_field->value_type = JSON_STRING;
    new_field->field_name = strdup(field_name);
    new_field->str_value = strdup(value);
    new_field->next_field = NULL;

    if (prev_field != NULL)
        prev_field->next_field = new_field;
    
    json->last = new_field;
    return json;
}

Json *Json_add_double_to_object(Json *json, char *field_name, double value) {
    JsonNode *prev_field = json->last;

    JsonNode *new_field = (JsonNode *) malloc(sizeof(JsonNode));
    new_field->value_type = JSON_DOUBLE;
    new_field->field_name = strdup(field_name);
    new_field->double_value = value;
    new_field->next_field = NULL;

    if (prev_field != NULL)
        prev_field->next_field = new_field;
    
    json->last = new_field;
    return json;
}

Json *Json_add_int_to_object(Json *json, char *field_name, int value) {
    JsonNode *prev_field = json->last;

    JsonNode *new_field = (JsonNode *) malloc(sizeof(JsonNode));
    new_field->value_type = JSON_INT;
    new_field->field_name = strdup(field_name);
    new_field->int_value = value;
    new_field->next_field = NULL;

    if (prev_field != NULL)
        prev_field->next_field = new_field;
    
    json->last = new_field;
    return json;
}

Json *Json_add_object_to_object(Json *json, char *field_name, Json *object) {
    JsonNode *prev_field = json->last;

    JsonNode *new_field = (JsonNode *) malloc(sizeof(JsonNode));
    new_field->value_type = JSON_OBJECT;
    new_field->field_name = strdup(field_name);
    new_field->object = object;
    new_field->next_field = NULL;

    if (prev_field != NULL)
        prev_field->next_field = new_field;
    
    json->last = new_field;
    return json;
}

int Json_get_string(Json *json, char *field_name, char *out);

int Json_get_int(Json *json, char *field_name, int *out);

int Json_get_double(Json *json, char *field_name, double *out);

void indent(StringBuffer *strbuf, char *indent_value, int indent_level) {
    for (int i = 0; i < indent_level; i++) {
        StringBuffer_append(strbuf, indent_value);
    }
}

char *Json_as_string_helper(Json *json, int indent_level) {
    static char *INDENT = "    ";

    StringBuffer *strbuf = StringBuffer_empty();
    
    indent(strbuf, INDENT, indent_level);
    StringBuffer_append(strbuf, "{\n");

    indent_level++;

    JsonNode *current_node = json->last;
    while (current_node != NULL) {
        indent(strbuf, INDENT, indent_level);

        switch (current_node->value_type) {
            case JSON_STRING:
                StringBuffer_append(strbuf, current_node->field_name);
                StringBuffer_append(strbuf, ": \"");
                StringBuffer_append(strbuf, current_node->str_value);
                StringBuffer_append(strbuf, "\"");
                break;
            case JSON_INT:
                // ...
                break;
            case JSON_DOUBLE:
                // ...
                break;
            case JSON_OBJECT:
                // ...
                break;
        }
    }

    indent(strbuf, INDENT, indent_level);
    StringBuffer_append(strbuf, "}");

    char *raw_buffer = strbuf->buffer;
    StringBuffer_delete(strbuf);
    return raw_buffer;
}

char *Json_as_string(Json *json);

#endif
