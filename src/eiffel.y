%{
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>

    #include "./include/json.h"

    extern int yylex(void);
    extern void yyrestart(FILE *infile);

    int errors_count = 0;
    Json *output_tree = NULL;

    void yyerror(const char *str) {
        errors_count++;
        fprintf(stderr, "Parser error: %s\n", str);
    }

    #define YYDEBUG 1

    #define LOG_NODE(msg) printf("Found node: %s\n", msg)

    void
    add_type_to_node(Json *node, char *type_name) {
        Json_add_string_to_object(node, "type", type_name);
    }

    Json*
    mk_int_const(int val) {
        Json *node = Json_new();
        add_type_to_node(node, "int_const");
        Json_add_int_to_object(node, "value", val);
        return node;
    }

    Json*
    mk_char_const(int val) {
        Json *node = Json_new();
        add_type_to_node(node, "char_const");
        Json_add_int_to_object(node, "value", val);
        return node;
    }

    Json*
    mk_real_const(double val) {
        Json *node = Json_new();
        add_type_to_node(node, "real_const");
        Json_add_double_to_object(node, "value", val);
        return node;
    }

    Json*
    mk_string_const(char *val) {
        Json *node = Json_new();
        add_type_to_node(node, "string_const");
        Json_add_string_to_object(node, "value", val);
        return node;
    }

    Json*
    mk_result_const() {
        Json *node = Json_new();
        add_type_to_node(node, "result_const");
        return node;
    }

    Json*
    mk_current_const() {
        Json *node = Json_new();
        add_type_to_node(node, "current_const");
        return node;
    }

    Json*
    mk_boolean_const(bool val) {
        Json *node = Json_new();
        add_type_to_node(node, "boolean_const");
        return node;
    }

    Json*
    mk_void_const() {
        Json *node = Json_new();
        add_type_to_node(node, "void_const");
        return node;
    }

    Json*
    mk_ident_lit(char *ident) {
        Json *node = Json_new();
        add_type_to_node(node, "ident_lit");
        Json_add_string_to_object(node, "value", ident);
        return node;
    }

    Json*
    mk_bin_op(char *op_name, Json *left, Json *right) {
        Json *node = Json_new();
        add_type_to_node(node, op_name);
        Json_add_object_to_object(node, "left", left);
        Json_add_object_to_object(node, "right", right);
        return node;
    }

    Json*
    mk_unary_op(char *op_name, Json *arg) {
        Json *node = Json_new();
        add_type_to_node(node, op_name);
        Json_add_object_to_object(node, "arg", arg);\
        return node;
    }

    Json*
    mk_args_list() {
        return Json_new();
    }

    Json*
    add_arg_to_list(Json *args_list, Json *arg) {
        Json_add_object_to_array(args_list, arg);
        return args_list;
    }

    Json*
    mk_simple_call(char *feature_name, Json *args_list) {
        Json *simple_call = Json_new();
        Json_add_string_to_object(simple_call, "name", feature_name);
        Json_add_array_to_object(simple_call, "args_list", args_list);
        return simple_call;
    }

    Json*
    mk_simple_call_no_args(char *feature_name) {
        return mk_simple_call(feature_name, mk_args_list());
    }

    Json*
    mk_precursor_args_call(Json *args_list) {
        Json *node = Json_new();
        add_type_to_node(node, "precursor_call");
        Json_add_array_to_object(node, "args_list", args_list);
        return node;
    }

    Json*
    mk_precursor_no_args_call() {
        return mk_precursor_args_call(mk_args_list());
    }

    Json*
    mk_feature_with_owner_call(Json *owner, Json *feature) {
        Json *node = Json_new();

        add_type_to_node(node, "feature_call");
        
        if (owner != NULL)
            Json_add_object_to_object(node, "owner", owner);
        else
            Json_add_null_to_object(node, "onwer");

        Json_add_object_to_object(node, "feature", feature);
        return node;
    }

    Json*
    mk_feature_with_unknown_owner_call(Json *feature) {
        return mk_feature_with_owner_call(NULL, feature);
    }

    Json*
    mk_bracket_access(Json *source, Json *index) {
        Json *node = Json_new();
        add_type_to_node(node, "bracket_access");
        Json_add_object_to_object(node, "source", source);
        Json_add_object_to_object(node, "index", index);
        return node;
    }

    Json*
    mk_if_expr(Json *cond, Json *then_expr, Json *alt_exprs, Json *else_expr) {
        Json *node = Json_new();
        add_type_to_node(node, "if_expr");
        Json_add_object_to_object(node, "cond", cond);
        Json_add_object_to_object(node, "then_expr", then_expr);
        Json_add_array_to_object(node, "alt_exprs", alt_exprs);
        Json_add_object_to_object(node, "else_expr", else_expr);
        return node;
    }

    Json*
    mk_elseif_expr_list() {
        return Json_new();
    }

    Json*
    add_alt_expr(Json *alts, Json *cond, Json *expr) {
        Json *alt = Json_new();
        Json_add_object_to_object(alt, "cond", cond);
        Json_add_object_to_object(alt, "expr", expr);
        Json_add_object_to_array(alts, alt);
        return alts;
    }

    Json*
    mk_assign_stmt(Json *left, Json *right) {
        Json *node = Json_new();
        add_type_to_node(node, "assign_stmt");
        Json_add_object_to_object(node, "left", left);
        Json_add_object_to_object(node, "right", right);
        return node;
    }
%}

%define parse.error verbose

%union {
    int int_value;
    double real_value;
    char *string_value;
    char *ident;
    struct Json *tree;
}

%start assign_stmt

%token EOI 0 "end of file"

%token <int_value> INT_CONST
%token <real_value> REAL_CONST
%token <ident> IDENT_LIT 
%token <int_value> CHAR_CONST
%token <string_value> STRING_CONST

%type <tree> constant expr

%type <tree> assign_stmt writable

%type <tree> simple_call precursor_call call
%type <tree> params_list comma_separated_exprs
%type <tree> bracket_access
%type <tree> if_expr elseif_expr_opt elseif_expr

%token INT_DIV MOD
%token AND OR NOT AND_THEN OR_ELSE
%token NEQ LE GE
%token ASSIGN_TO
%token END
%token IF THEN ELSEIF ELSE
%token FROM UNTIL LOOP
%token WHEN INSPECT TWO_DOTS
%token CLASS
%token LIKE
%token DO
%token INTEGER REAL STRING_KW CHARACTER BOOLEAN ARRAY TUPLE
%token FEATURE CREATE
%token LOCAL
%token REQUIRE ENSURE
%token CURRENT PRECURSOR RESULT
%token RARROW
%token AS INHERIT REDEFINE RENAME UNDEFINE SELECT
%token TRUE_KW FALSE_KW VOID

%nonassoc ASSIGN_TO
%nonassoc LOWER_THAN_EXPR
%nonassoc LOWER_THAN_PARENS
%nonassoc '(' ')'
%right IMPLIES
%left OR OR_ELSE XOR
%left AND AND_THEN
%right NOT
%left '<' '>' LE GE '=' NEQ
%left '+' '-'
%left '*' '/' INT_DIV MOD
%right '^'
%nonassoc UMINUS UPLUS
%left '[' ']'
%right '.'

%%

/* ********************************************************************/
/* Описание программы */
program: class_list
       ;

/* ********************************************************************/
/* Описание класса */
class_list: class_declaration
          | class_list class_declaration
          ;

class_declaration: class_header inheritance_opt creators_opt class_feature_opt END
                 ;

/* Заголовок класса */
class_header: CLASS IDENT_LIT formal_generics_opt
            ;

formal_generics_opt: /* empty */
                   | '[' formal_generics ']'
                   ;

formal_generics: generic
               | formal_generics ',' generic
               ;

generic: type
       | type RARROW type
       ;

/* Секция конструкторов */
creators_opt: /* empty */
            | creators
            ;

creators: CREATE ident_list
        ;


/* ********************************************************************/
/* Секция наследования */
inheritance_opt: /* empty */
               | INHERIT inheritance
               ;

inheritance: inheritance_clause
           | inheritance inheritance_clause
           ;

inheritance_clause: parent
                  | parent rename_clause undefine_clause_opt redefine_clause_opt select_clause_opt END
                  | parent undefine_clause redefine_clause_opt select_clause_opt END
                  | parent redefine_clause select_clause_opt END
                  | parent select_clause END
                  ;

parent: IDENT_LIT formal_generics_opt
      ;

/* Секция переименования */
rename_clause: RENAME rename_list
             ;

rename_list: IDENT_LIT AS IDENT_LIT
           | rename_list IDENT_LIT AS IDENT_LIT
           ;


/* Секция undefine */
undefine_clause_opt: /* empty */
                   | undefine_clause
                   ;

undefine_clause: UNDEFINE ident_list
               ;


/* Секция переопределения */
redefine_clause_opt: /* empty */
                   | redefine_clause
                   ;

redefine_clause: REDEFINE ident_list
               ;


/* Секция select */
select_clause_opt: /* empty */
                 | select_clause
                 ;

select_clause: SELECT ident_list
             ;


/* ********************************************************************/
/* Описание feature класса */
class_feature_opt: /* empty */
                 | class_feature
                 ;

class_feature: FEATURE clients_opt feature_list
             | class_feature FEATURE clients_opt feature_list
             ;

clients_opt: /* empty */
           | clients
           ;

clients: '{' ident_list '}'
       ;


/* ********************************************************************/
/* Описание типов */
type: IDENT_LIT
    | INTEGER
    | REAL
    | STRING_KW
    | CHARACTER
    | BOOLEAN
    | LIKE CURRENT
    | LIKE IDENT_LIT
    | generic_type
    ;

generic_type: IDENT_LIT '[' type_list ']'
            | ARRAY '[' type ']'
            | TUPLE '[' type_list ']'
            ;

type_list: type
         | type_list ';' type
         ;


/* ********************************************************************/
/* Описания для полей и методов класса */
feature_list: feature
            | feature_list feature
            ;

/*
Поддерживаются:
1) Объявление вида (атрибуты): a, b: INTEGER

2) Методы, не принимающие параметров и ничего не возвращающие:
    a, b, c do
        ...
    end

3) Указание метода, ничего не принимающего, но возвращающего что-то:
    f: REAL do
        ...
    end

4) Указание аргументов:
    f (a: INTEGER, b: REAL) do
        ...
    end

    Пустые скобки также поддерживаются

5) Все вместе:
    f, g (a: INTEGER, b: REAL): STRING do
        ...
    end
*/
feature: name_and_type
       | ident_list routine_body
       | name_and_type routine_body 
       | ident_list '(' args_list_opt ')' routine_body
       | ident_list '(' args_list_opt ')' type_spec routine_body
       ;

/* Список имен с заданным типом */
name_and_type: ident_list type_spec
             ;

ident_list: IDENT_LIT
          | ident_list ',' IDENT_LIT

type_spec: ':' type
         ;

/* Список аргументов */
args_list_opt: /* empty */
             | args_list
             ;

args_list: name_and_type
         | args_list ';' name_and_type
         ;

/* Тело метода */
routine_body: local_part_opt require_part_opt do_part ensure_part_opt END
            ;

/* Секция объявления локальных переменных */
local_part_opt: /* empty */
              | local_part
              ;

local_part: LOCAL var_decl_list
          ;

var_decl_list: name_and_type
             | var_decl_list name_and_type
             ;

/* Секция предусловий */
require_part_opt: /* empty */
                | require_part
                ;

require_part: REQUIRE condition_list
            ;

condition_list: condition
              | condition_list condition
              | condition_list ';' condition
              ;

/*
Необходимо сделать приоритет данных правил ниже чем expr,
т.к. возникают shift/reduce конфликты со следующим примером: require 3 + 4
Либо это один condition, либо два (3 и +4). Несмотря на то, что эта конструкция
некорректна (с точки зрения семантики), нужно убедится, что даже она распознает правильно
*/
condition: expr %prec LOWER_THAN_EXPR
         | IDENT_LIT ':' expr %prec LOWER_THAN_EXPR
         ;

/* Секция инструкций метода */
do_part: DO stmt_list_opt
       ;

/* Секция постусловий  */
ensure_part_opt: /* empty */
               | ensure_part
               ;

ensure_part: ENSURE condition_list
           ;


/* ********************************************************************/
/* Описание инструкций */
stmt_list_opt: /* empty */
             | stmt_list { LOG_NODE("stmt_list_opt"); }
             ;

stmt_list: stmt
         | stmt_list stmt
         ;

stmt: assign_stmt
    | if_stmt
    | loop_stmt
    | inspect_stmt
    | call
    | ';'
    ;


/* ********************************************************************/
/* Описание оператора присваивания */
assign_stmt: writable ASSIGN_TO expr { $$ = mk_assign_stmt($1, $3); output_tree = $$; }
           ;

writable: IDENT_LIT { $$ = mk_ident_lit($1); }
        | RESULT { $$ = mk_result_const(); }
        | bracket_access { $$ = $1; }
        ;


/* ********************************************************************/
/* Описание оператора цикла */
loop_stmt: FROM stmt_list_opt UNTIL expr LOOP stmt_list_opt END
         ;


/* ********************************************************************/
/* Описание оператора выбора */
inspect_stmt: INSPECT expr when_clauses_opt else_clause_opt END
            ;

when_clauses_opt: /* empty */
                | when_clauses
                ;

when_clauses: WHEN choices_opt THEN stmt_list_opt
            | when_clauses WHEN choices_opt THEN stmt_list_opt
            ;

choices_opt: /* empty */
           | choices
           ;

choices: choice
       | choices ',' choice
       ;

choice: expr
      | expr TWO_DOTS expr
      ;


/* ********************************************************************/
/* Описание оператора ветвления */
if_stmt: IF expr THEN stmt_list_opt elseif_clauses_opt else_clause_opt END
       ;

elseif_clauses_opt: /* empty */
                  | elseif_clauses
                  ;

elseif_clauses: ELSEIF expr THEN stmt_list_opt
              | elseif_clauses ELSEIF expr THEN stmt_list_opt

else_clause_opt: /* empty */
               | ELSE stmt_list_opt
               ;

/* ********************************************************************/
/* Описание вызова метода */

/*
Поддерживаются:
1) Обычный вызов со скобками и без: g(a, b, c); f(); fi
2) Вызов метода родительского класса с тем же именем: Precursor(1, 2, 3)
3) Через Result: Result.f(a, b)
4) Вызов метода у объекта через Current: Current.f(a, b)
5) У произвольного выражения в круглых скобках: (1 + 2).out
6) Вызов метода у элемента массива: numbers[1].to_natural_8
7) Вызовы произвольной вложенности: Result.f.g(a, b, c)
*/
call: simple_call { $$ = mk_feature_with_unknown_owner_call($1); }
    | precursor_call { $$ = $1; }
    | RESULT         '.' simple_call { $$ = mk_feature_with_owner_call(mk_result_const(), $3); }
    | CURRENT        '.' simple_call { $$ = mk_feature_with_owner_call(mk_current_const(), $3); }
    | '(' expr ')'   '.' simple_call { $$ = mk_feature_with_owner_call($2, $5); }
    | bracket_access '.' simple_call { $$ = mk_feature_with_owner_call($1, $3); }
    | call           '.' simple_call { $$ = mk_feature_with_owner_call($1, $3); }
    ;

precursor_call: PRECURSOR %prec LOWER_THAN_EXPR { $$ = mk_precursor_no_args_call(); }
              | PRECURSOR '(' params_list ')' { $$ = mk_precursor_args_call($3); }
              ;

simple_call: IDENT_LIT %prec LOWER_THAN_PARENS { $$ = mk_simple_call_no_args($1); }
           | IDENT_LIT '(' params_list ')' { $$ = mk_simple_call($1, $3); }
           ;

params_list: /* empty */ { $$ = mk_args_list(); }
           | comma_separated_exprs { $$ = $1; }
           ;

comma_separated_exprs: expr { $$ = mk_args_list(); $$ = add_arg_to_list($$, $1); }
                     | comma_separated_exprs ',' expr { $$ = add_arg_to_list($1, $3); }
                     ;


/* ********************************************************************/
/* Тернарный оператор */
if_expr: IF expr THEN expr elseif_expr_opt ELSE expr END { $$ = mk_if_expr($2, $4, $5, $7); }

elseif_expr_opt: /* empty */ { $$ = mk_elseif_expr_list();  }
               | elseif_expr { $$ = $1; }

elseif_expr: ELSEIF expr THEN expr { $$ = mk_elseif_expr_list(); $$ = add_alt_expr($$, $2, $4); }
           | elseif_expr ELSEIF expr THEN expr { $$ = add_alt_expr($1, $3, $5); }


/* ********************************************************************/
/* Описание выражений */

/* Взятие элемента через квадратный скобки */
bracket_access: call '[' expr ']' { $$ = mk_bracket_access($1, $3); }
              | bracket_access '[' expr ']' { $$ = mk_bracket_access($1, $3); }
              ;

/* Константы */
constant: INT_CONST     { $$ = mk_int_const($1); }
        | REAL_CONST    { $$ = mk_real_const($1); }
        | CHAR_CONST    { $$ = mk_char_const($1); }
        | STRING_CONST  { $$ = mk_string_const($1); }
        | RESULT        { $$ = mk_result_const(); }
        | CURRENT       { $$ = mk_current_const(); }
        | TRUE_KW       { $$ = mk_boolean_const(true); } 
        | FALSE_KW      { $$ = mk_boolean_const(false); } 
        | VOID          { $$ = mk_void_const(); }
        ;

expr: constant { $$ = $1; }
    | expr '+' expr { $$ = mk_bin_op("add_op", $1, $3); }
    | expr '-' expr { $$ = mk_bin_op("sub_op", $1, $3); }       
    | expr '*' expr { $$ = mk_bin_op("mul_op", $1, $3); }       
    | expr '/' expr { $$ = mk_bin_op("div_op", $1, $3); }       
    | '(' expr ')'  { $$ = $2; }
    | '+' expr %prec UPLUS { $$ = mk_unary_op("unary_plus_op", $2); }
    | '-' expr %prec UMINUS { $$ = mk_unary_op("unary_minus_op", $2); }
    | expr INT_DIV expr { $$ = mk_bin_op("int_div_op", $1, $3); }
    | expr MOD expr { $$ = mk_bin_op("mod_op", $1, $3); }       
    | expr '^' expr { $$ = mk_bin_op("exp_op", $1, $3); }
    | expr AND expr { $$ = mk_bin_op("and_op", $1, $3); }       
    | expr OR expr { $$ = mk_bin_op("or_op", $1, $3); }         
    | NOT expr { $$ = mk_unary_op("not_op", $2); }            
    | expr AND_THEN expr { $$ = mk_bin_op("and_then_op", $1, $3); }
    | expr OR_ELSE expr { $$ = mk_bin_op("or_else_op", $1, $3); }  
    | expr XOR expr { $$ = mk_bin_op("xor_op", $1, $3); }       
    | expr '<' expr { $$ = mk_bin_op("lt_op", $1, $3); }          
    | expr '>' expr { $$ = mk_bin_op("gt_op", $1, $3); }       
    | expr '=' expr { $$ = mk_bin_op("eq_op", $1, $3); }       
    | expr LE expr  { $$ = mk_bin_op("le_op", $1, $3); }       
    | expr GE expr  { $$ = mk_bin_op("ge_op", $1, $3); }       
    | expr NEQ expr { $$ = mk_bin_op("neq_op", $1, $3); }       
    | expr IMPLIES expr { $$ = mk_bin_op("implies_op", $1, $3); }
    | call { $$ = $1; }
    | bracket_access { $$ = $1; }
    | if_expr { $$ = $1; } 
    ;
%%

bool
write_output_tree(char *file_name) {
    char *json = Json_object_as_string(output_tree);

    if (file_name == NULL) {
        printf(json);
        return 1;
    }

    FILE *output_file = fopen(file_name, "w");
    if (output_file == NULL)
        return 0;

    fprintf(output_file, json);
    fclose(output_file);

    return 1;
}

void
show_parsing_result(int errors_count) {
    if (errors_count > 0) {
        if (errors_count == 1)
            puts("Failed to parse, got 1 syntax error");
        else
            printf("Failed to parse, got %d syntax errors\n", errors_count);
    }
}

void
parse_files(int files_count, char **file_names) {
    if (files_count == 0) {
        yyparse();
        return;
    }

    for (int i = 0; i < files_count; i++) {
        FILE *eiffel_file = fopen(file_names[i], "r");
        if (eiffel_file == NULL) {
            perror(file_names[i]);
            continue;
        }

        yyrestart(eiffel_file);
        yyparse();
    }
}

int
main(int argc, char **argv) {
    #ifdef DEBUG_PARSER
        yydebug = 1;
    #endif

    parse_files(argc - 1, argv + 1);

    show_parsing_result(errors_count);
    
    if (errors_count == 0) {
        write_output_tree(NULL);
        return EXIT_SUCCESS;
    }

    return EXIT_FAILURE;
}
