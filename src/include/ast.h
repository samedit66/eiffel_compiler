#include "json.h"

/**
 * Создает "пустой" узел. Используется для указания отсутствия
 * значения у какого-либо узла, либо для создания пустого оператора
 * (например, точка с запятой (;) транслируется в пустой узел)
 * 
 * @return Пустой узел
 */
Json*
mk_empty();

/**
 * Создает узел константы целого числа
 * 
 * @param val Значение целого числа
 * @return Узел с константой целого числа
 */
Json*
mk_int_const(int val);

/**
 * Создает узел константы символа
 * 
 * @param val Числовой код символа (int)
 * @return Узел с константой символа
 */
Json*
mk_char_const(int val);

/**
 * Создает узел константы вещественного числа
 * 
 * @param val Значение вещественного числа
 * @return Узел с константой вещественного числа
 */
Json*
mk_real_const(double val);

/**
 * Создает узел строковой константы
 * 
 * @param val Значение строки
 * @return Узел со строковой константой
 */
Json*
mk_string_const(char *val);

/**
 * Создает узел константы результата
 * 
 * @return Узел с константой результата
 */
Json*
mk_result_const();

/**
 * Создает узел константы указателя на текущий экземпляр объекта
 * 
 * @return Узел с константой указателя на текущий экземпляр объекта
 */
Json*
mk_current_const();

/**
 * Создает узел булевой константы
 * 
 * @param val Значение булевой переменной
 * @return Узел с булевой константой
 */
Json*
mk_boolean_const(bool val);

/**
 * Создает узел пустой константы (void)
 * 
 * @return Узел пустой константы
 */
Json*
mk_void_const();

/**
 * Создает узел идентификатора
 * 
 * @param ident Значение идентификатора
 * @return Узел с идентификатором
 */
Json*
mk_ident_lit(char *ident);

/**
 * Создает узел бинарной операции
 * 
 * @param op_name Имя операции
 * @param left Левый операнд
 * @param right Правый операнд
 * @return Узел бинарной операции
 */
Json*
mk_bin_op(char *op_name, Json *left, Json *right);

/**
 * Создает узел унарной операции
 * 
 * @param op_name Имя операции
 * @param arg Операнд
 * @return Узел унарной операции
 */
Json*
mk_unary_op(char *op_name, Json *arg);

/**
 * Создает узел простого вызова с аргументами без указания выладельца метода
 * 
 * @param feature_name Имя вызываемой функции
 * @param args_list Список аргументов
 * @return Узел простого вызова
 */
Json*
mk_simple_call(char *feature_name, Json *args_list);

/**
 * Создает пустой список. Применяется для указания аргументов функции,
 * последовательности стейтментов, последователи альтернативных ветвей ветвления
 * и так далее
 * 
 * @return Пустой список
 */
Json*
mk_list();

/**
 * Добавляет элемент в список.
 * 
 * @param list Список JSON
 * @param element Добавляемый элемент
 * @return Список JSON с добавленным элементом
 */
Json*
add_to_list(Json *list, Json *element);

/**
 * Создает узел простого вызова без аргументов
 * 
 * @param feature_name Имя вызываемой функции
 * @return Узел простого вызова без аргументов
 */
Json*
mk_simple_call_no_args(char *feature_name);

/**
 * Создает узел вызова предка с аргументами
 * 
 * @param args_list Список аргументов
 * @return Узел вызова предка с аргументами
 */
Json*
mk_precursor_args_call(Json *args_list);

/**
 * Создает узел вызова метода родителя с тем же именем без аргументов
 * 
 * @return Узел вызова метода родителя с тем же именем без аргументов
 */
Json*
mk_precursor_no_args_call();

/**
 * Создает узел вызова метода с указанием владельца метода
 * 
 * @param owner Владелец. Может быть NULL, тогда создается узел с пустым владельцем
 * @param feature Метод
 * @return Узел вызова метода с указанием владельца метода
 */
Json*
mk_feature_with_owner_call(Json *owner, Json *feature);

/**
 * Создает узел вызова функции с неизвестным владельцем.
 * 
 * @param feature Метод
 * @return Узел вызова функции с неизвестным владельцем
 */
Json*
mk_feature_with_unknown_owner_call(Json *feature);

/**
 * Создает узел доступа по скобкам
 * 
 * @param source Источника
 * @param index Индекса
 * @return Узел доступа по скобкам
 */
Json*
mk_bracket_access(Json *source, Json *index);

/**
 * Создает узел выражения "if"
 * 
 * @param cond Условие
 * @param then_expr Узел "then" выражения
 * @param alt_exprs Список альтернативных выражений (elseif)
 * @param else_expr Узел "else" выражения
 * @return Узел выражения "if"
 */
Json*
mk_if_expr(Json *cond, Json *then_expr, Json *alt_exprs, Json *else_expr);

/**
 * Добавляет узел выражения "elseif" к списку альтернативных выражений
 * 
 * @param alts Список альтернативных выражений
 * @param cond Узел условия
 * @param expr Узел выражения
 * @return Обновленный список альтернативных выражений
 */
Json*
add_elseif_expr(Json *alts, Json *cond, Json *expr);

/**
 * Создает корневой узел программы.
 * 
 * @param program Узел программы - список различных узлов
 * @return Корневой узел программы
 */
Json*
mk_program(Json *program);

/**
 * Создает узел оператора "if"
 * 
 * @param cond Условие
 * @param then_stmt_list Список операторов "then"
 * @param alt_stmts Узел списка альтернативных операторов (elseif)
 * @param else_stmt_list Список операторов "else"
 * @return Узел оператора "if"
 */
Json*
mk_if_stmt(Json *cond, Json *then_stmt_list, Json *alt_stmts, Json *else_stmt_list);

/**
 * Добавляет узел "elseif" к списку альтернативных операторов
 * 
 * @param alts Список альтернативных операторов
 * @param cond Условие
 * @param stmt_list Список операторов
 * @return Обновленный список альтернативных операторов
 */
Json*
add_elseif_stmt(Json *alts, Json *cond, Json *stmt_list);

/**
 * Создает узел оператора присваивания
 * 
 * @param left Левый операнд
 * @param right Правый операнд
 * @return Узел оператора присваивания
 */
Json*
mk_assign_stmt(Json *left, Json *right);

/**
 * Создает узел оператора цикла
 * 
 * @param init_stmt_list Список начальных операторов
 * @param cond Узел условия
 * @param body_stmt_list Список операторов тела цикла
 * @return Узел оператора цикла
 */
Json*
mk_loop_stmt(Json *init_stmt_list, Json *cond, Json *body_stmt_list);

/**
 * Создает узел оператора "inspect"
 * 
 * @param expr Выражение для проверки
 * @param when_clauses Список операторов "when"
 * @param else_stmt_list Список операторов "else"
 * @return Узел оператора "inspect"
 */
Json*
mk_inspect_stmt(Json *expr, Json *when_clauses, Json *else_stmt_list);

/**
 * Добавляет узел "when" к списку операторов
 * 
 * @param when_clauses Список операторов "when"
 * @param choices Список условий
 * @param body Список операторов
 * @return Обновленный список операторов "when"
 */
Json*
add_alt_when_clause(Json *when_clauses, Json *choices, Json *body);

/**
 * Создает узел интервала выбора для оператора inspect
 * 
 * @param start Начальное значение
 * @param end Конечное значение
 * @return Узел интервала выбора
 */
Json*
mk_choice_interval(Json *start, Json *end);

/**
 * Создает узел типа
 * 
 * @param type_name Имя типа
 * @return Узел типа
 */
Json*
mk_type(char *type_name);

/**
 * Создает узел встроенного типа "INTEGER"
 * 
 * @return Узел встроенного типа "INTEGER"
 */
Json*
mk_integer_type();

/**
 * Создает узел встроенного типа "REAL".
 * 
 * @return Узел встроенного типа "REAL"
 */
Json*
mk_real_type();

/**
 * Создает узел встроенного типа "STRING".
 * 
 * @return Узел встроенного типа "STRING"
 */
Json*
mk_string_type();

/**
 * Создает узел встроенного типа "CHARACTER".
 * 
 * @return Узел встроенного типа "CHARACTER"
 */
Json*
mk_character_type();

/**
 * Создает узел встроенного типа "BOOLEAN"
 * 
 * @return Узел встроенного типа "BOOLEAN"
 */
Json*
mk_boolean_type();

/**
 * Создает узел типа "LIKE"
 * 
 * @param like_what Узел, от которого наследуется тип
 * @return Узел типа "LIKE"
 */
Json*
mk_like_type(Json *like_what);

/**
 * Создает узел типа "LIKE Current"
 * 
 * @return Узел типа "LIKE Current"
 */
Json*
mk_like_current_type();

/**
 * Создает узел типа "LIKE other_field"
 * 
 * @param field_name Имя поля
 * @return Узел типа "LIKE other_field"
 */
Json*
mk_like_other_field_type(char *field_name);

/**
 * Создает узел пользовательского обобщенного типа
 * 
 * @param type_name Имя типа
 * @param type_list Список типов
 * @return Узел обобщенного типа
 */
Json*
mk_generic_user_type(char *type_name, Json *type_list);

/**
 * Создает узел обобщенного типа "ARRAY"
 * 
 * @param type_list Список типов
 * @return Узел типа "ARRAY"
 */
Json*
mk_generic_array_type(Json *type_list);

/**
 * Создает узел обобщенного типа "TUPLE"
 *
 * @param type_list Список типов
 * @return Узел типа "TUPLE"
 */
Json*
mk_generic_tuple_type(Json *type_list);

/**
 * Создает узел объявления класса
 * 
 * @param header Заголовок класса
 * @param inheritance Секция наследования
 * @param creators Секция конструкторов
 * @param features Секция методов и полей класса
 */
Json*
mk_class_decl(Json *header, Json *inheritance, Json *creators, Json *features);

Json*
mk_class_header(char *class_name, Json *generics_list);

Json*
mk_constrained_generic(Json *generic_type, Json *parent);
