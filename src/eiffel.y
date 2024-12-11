%{
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>

    #include "./include/ast.h"

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
%}

%define parse.error verbose

%union {
    int int_value;
    double real_value;
    char *string_value;
    char *ident;
    struct Json *tree;
}

%start program

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

%type <tree> stmt stmt_list stmt_list_opt
%type <tree> loop_stmt
%type <tree> inspect_stmt
%type <tree> when_clauses_opt when_clauses choices_opt choices choice
%type <tree> if_stmt elseif_clauses_opt elseif_clauses else_clause_opt

%type <tree> feature_list feature
%type <tree> name_and_type type_spec routine_body

%type <tree> class_declaration class_header inheritance_opt creators_opt features_clause_opt
%type <tree> formal_generics_opt formal_generics generic
%type <tree> creators
%type <tree> inheritance inheritance_clause parent rename_clause undefine_clause_opt redefine_clause_opt select_clause_opt
%type <tree> rename_list
%type <tree> undefine_clause
%type <tree> redefine_clause
%type <tree> select_clause
%type <tree> features_clause clients_opt clients

%type <tree> ident_list

%type <tree> type generic_type type_list

%type <tree> class_list

%type <tree> program

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

%nonassoc FIELD
%nonassoc ROUTINE
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
program: class_list { $$ = mk_program($1); output_tree = $$; }
       ;

/* ********************************************************************/
/* Описание класса */
class_list: class_declaration { $$ = mk_list(); $$ = add_to_list($$, $1); }
          | class_list class_declaration { $$ = add_to_list($1, $2);  }
          ;

class_declaration: class_header inheritance_opt creators_opt features_clause_opt END { $$ = mk_class_decl($1, $2, $3, $4); }
                 ;

/* Заголовок класса */
class_header: CLASS IDENT_LIT formal_generics_opt { $$ = mk_class_header($2, $3); }
            ;

formal_generics_opt: /* empty */ { $$ = mk_list(); }
                   | '[' formal_generics ']' { $$ = $2; }
                   ;

formal_generics: generic { $$ = mk_list(); $$ = add_to_list($$, $1); }
               | formal_generics ',' generic { $$ = add_to_list($1, $3); }
               ;

generic: type { $$ = $1; }
       | type RARROW type { $$ = mk_constrained_generic($1, $3); }
       ;

/* Секция конструкторов */
creators_opt: /* empty */ { $$ = mk_list(); }
            | creators { $$ = $1; }
            ;

creators: CREATE ident_list { $$ = $2; }
        ;


/* ********************************************************************/
/* Секция наследования */
inheritance_opt: /* empty */ { $$ = mk_list(); }
               | INHERIT inheritance { $$ = $2; }
               ;

inheritance: inheritance_clause { $$ = mk_list(); $$ = add_to_list($$, $1); }
           | inheritance inheritance_clause { $$ = add_to_list($1, $2); }
           ;

inheritance_clause: parent { $$ = mk_inherit_clause($1, mk_list(), mk_list(), mk_list(), mk_list()); }
                  | parent rename_clause undefine_clause_opt redefine_clause_opt select_clause_opt END { $$ = mk_inherit_clause($1, $2, $3, $4, $5); }
                  | parent undefine_clause redefine_clause_opt select_clause_opt END { $$ = mk_inherit_clause($1, mk_list(), $2, $3, $4); }
                  | parent redefine_clause select_clause_opt END { $$ = mk_inherit_clause($1, mk_list(), mk_list(), $2, $3); }
                  | parent select_clause END { $$ = mk_inherit_clause($1, mk_list(), mk_list(), mk_list(), $2); }
                  ;

parent: IDENT_LIT formal_generics_opt { $$ = mk_class_header($1, $2); }
      ;

/* Секция переименования */
rename_clause: RENAME rename_list { $$ = $2; }
             ;

rename_list: IDENT_LIT AS IDENT_LIT { $$ = mk_list(); $$ = add_to_list($$, mk_alias($1, $3)); }
           | rename_list IDENT_LIT AS IDENT_LIT { $$ = add_to_list($1, mk_alias($2, $4)); }
           ;


/* Секция undefine */
undefine_clause_opt: /* empty */ { $$ = mk_list(); }
                   | undefine_clause { $$ = $1; }
                   ;

undefine_clause: UNDEFINE ident_list { $$ = $2; }
               ;


/* Секция переопределения */
redefine_clause_opt: /* empty */ { $$ = mk_list(); }
                   | redefine_clause { $$ = $1; }
                   ;

redefine_clause: REDEFINE ident_list { $$ = $2;  }
               ;


/* Секция select */
select_clause_opt: /* empty */ { $$ = mk_list(); }
                 | select_clause { $$ = $1; }
                 ;

select_clause: SELECT ident_list { $$ = $2; }
             ;


/* ********************************************************************/
/* Описание feature класса */
features_clause_opt: /* empty */ { $$ = mk_list(); }
                   | features_clause { $$ = $1; }
                   ;

features_clause: FEATURE clients_opt feature_list { $$ = add_to_list(mk_list(), mk_feature_clause($2, $3)); }
               | features_clause FEATURE clients_opt feature_list { $$ = add_to_list($1, mk_feature_clause($3, $4)); }
               ;

clients_opt: /* empty */ { $$ = mk_list(); }
           | clients { $$ = $1; }
           ;

clients: '{' ident_list '}' { $$ = $2; }
       ;


/* ********************************************************************/
/* Описание типов */
type: IDENT_LIT { $$ = mk_type($1); }
    | INTEGER { $$ = mk_integer_type(); }
    | REAL { $$ = mk_real_type(); }
    | STRING_KW { $$ = mk_string_type(); }
    | CHARACTER { $$ = mk_character_type(); }
    | BOOLEAN { $$ = mk_boolean_type(); }
    | LIKE CURRENT { $$ = mk_like_current_type(); }
    | LIKE IDENT_LIT { $$ = mk_like_other_field_type($2); }
    | generic_type { $$ = $1; }
    ;

generic_type: IDENT_LIT '[' type_list ']' { $$ = mk_generic_user_type($1, $3); }
            | ARRAY '[' type ']' { $$ = mk_generic_array_type($3); }
            | TUPLE '[' type_list ']' { $$ = mk_generic_tuple_type($3); }
            ;

type_list: type { $$ = mk_list(); $$ = add_to_list($$, $1); }
         | type_list ';' type { $$ = add_to_list($1, $3);  }
         ;


/* ********************************************************************/
/* Описания для полей и методов класса */
feature_list: feature { $$ = add_to_list(mk_list(), $1); }
            | feature_list feature { $$ = add_to_list($1, $2); }
            ;

/*
Поддерживаются:
1) Объявление вида (атрибуты): a, b: INTEGER

2) Указание константных атрибутов класса: pi: REAL = 3.14

3) Методы, не принимающие параметров и ничего не возвращающие:
    a, b, c do
        ...
    end

4) Указание метода, ничего не принимающего, но возвращающего что-то:
    f: REAL do
        ...
    end

5) Указание аргументов:
    f (a: INTEGER, b: REAL) do
        ...
    end

    Пустые скобки также поддерживаются

6) Все вместе:
    f, g (a: INTEGER, b: REAL): STRING do
        ...
    end
*/
feature: name_and_type { $$ = mk_class_field($1); }
       | name_and_type '=' constant { $$ = mk_class_constant($1, $3); }
       | ident_list routine_body { $$ = mk_void_routine($1, $2); }
       | name_and_type routine_body { $$ = mk_routine($1, mk_list(), $2); }
       | ident_list '(' args_list_opt ')' routine_body
       | ident_list '(' args_list_opt ')' type_spec routine_body
       ;

/* Список имен с заданным типом */
name_and_type: ident_list type_spec { $$ = mk_name_and_type($1, $2); }
             ;

ident_list: IDENT_LIT { $$ = mk_list(); $$ = add_ident_to_list($$, $1); }
          | ident_list ',' IDENT_LIT { $$ = add_ident_to_list($1, $3); }

type_spec: ':' type { $$ = $2; }
         ;

/* Список аргументов */
args_list_opt: /* empty */
             | args_list
             ;

args_list: name_and_type
         | args_list ';' name_and_type
         ;

/* Тело метода */
routine_body: local_part_opt require_part_opt do_part then_part_opt ensure_part_opt END
            | local_part_opt require_part_opt then_part ensure_part_opt END
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

/* Секция then */
then_part_opt: /* empty */
             | then_part
             ;

then_part: THEN expr
         ;

/* Секция постусловий  */
ensure_part_opt: /* empty */
               | ensure_part
               ;

ensure_part: ENSURE condition_list
           ;


/* ********************************************************************/
/* Описание инструкций */
stmt_list_opt: /* empty */ { $$ = mk_list(); }
             | stmt_list   { $$ = $1; }
             ;

stmt_list: stmt           { $$ = mk_list(); $$ = add_to_list($$, $1); }
         | stmt_list stmt { $$ = add_to_list($1, $2); }
         ;

stmt: assign_stmt  { $$ = $1; }
    | if_stmt      { $$ = $1; }
    | loop_stmt    { $$ = $1; }
    | inspect_stmt { $$ = $1;}
    | call         { $$ = $1; }
    | ';'          { $$ = mk_empty(); }
    ;


/* ********************************************************************/
/* Описание оператора присваивания */
assign_stmt: writable ASSIGN_TO expr { $$ = mk_assign_stmt($1, $3);  }
           ;

writable: IDENT_LIT { $$ = mk_ident_lit($1); }
        | RESULT { $$ = mk_result_const(); }
        | bracket_access { $$ = $1; }
        ;


/* ********************************************************************/
/* Описание оператора цикла */
loop_stmt: FROM stmt_list_opt UNTIL expr LOOP stmt_list_opt END { $$ = mk_loop_stmt($2, $4, $6); }
         ;


/* ********************************************************************/
/* Описание оператора выбора */
inspect_stmt: INSPECT expr when_clauses_opt else_clause_opt END { $$ = mk_inspect_stmt($2, $3, $4); }
            ;

when_clauses_opt: /* empty */  { $$ = mk_list(); }
                | when_clauses { $$ = $1; }
                ;

when_clauses: WHEN choices_opt THEN stmt_list_opt { $$ = mk_list(); $$ = add_alt_when_clause($$, $2, $4); }
            | when_clauses WHEN choices_opt THEN stmt_list_opt { $$ = add_alt_when_clause($1, $3, $5); }
            ;

choices_opt: /* empty */ { $$ = mk_list(); }
           | choices { $$ = $1; }
           ;

choices: choice { $$ = mk_list(); $$ = add_to_list($$, $1); }
       | choices ',' choice { $$ = add_to_list($1, $3);  }
       ;

choice: expr { $$ = $1; }
      | expr TWO_DOTS expr { $$ = mk_choice_interval($1, $3); }
      ;


/* ********************************************************************/
/* Описание оператора ветвления */
if_stmt: IF expr THEN stmt_list_opt elseif_clauses_opt else_clause_opt END { $$ = mk_if_stmt($2, $4, $5, $6); }
       ;

elseif_clauses_opt: /* empty */    { $$ = mk_list(); }
                  | elseif_clauses { $$ = $1; }
                  ;

elseif_clauses: ELSEIF expr THEN stmt_list_opt { $$ = mk_list(); $$ = add_elseif_stmt($$, $2, $4); }
              | elseif_clauses ELSEIF expr THEN stmt_list_opt { $$ = add_elseif_stmt($1, $3, $5); }

else_clause_opt: /* empty */        { $$ = mk_list(); }
               | ELSE stmt_list_opt { $$ = $2; }
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

params_list: /* empty */ { $$ = mk_list(); }
           | comma_separated_exprs { $$ = $1; }
           ;

comma_separated_exprs: expr { $$ = mk_list(); $$ = add_to_list($$, $1); }
                     | comma_separated_exprs ',' expr { $$ = add_to_list($1, $3); }
                     ;


/* ********************************************************************/
/* Тернарный оператор */
if_expr: IF expr THEN expr elseif_expr_opt ELSE expr END { $$ = mk_if_expr($2, $4, $5, $7); }

elseif_expr_opt: /* empty */ { $$ = mk_list();  }
               | elseif_expr { $$ = $1; }

elseif_expr: ELSEIF expr THEN expr { $$ = mk_list(); $$ = add_elseif_expr($$, $2, $4); }
           | elseif_expr ELSEIF expr THEN expr { $$ = add_elseif_expr($1, $3, $5); }


/* ********************************************************************/
/* Описание выражений */

/* Взятие элемента через квадратный скобки */
bracket_access: call '[' expr ']' { $$ = mk_bracket_access($1, $3); }
              | constant '[' expr ']' { $$ = mk_bracket_access($1, $3); }
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
    free(json);

    return 1;
}

void
show_parsing_result(int errors_count) {
    if (errors_count == 1)
        puts("Failed to parse, got 1 syntax error");
    else if (errors_count > 1)
        printf("Failed to parse, got %d syntax errors\n", errors_count);
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

    // Пропускаем имя программы в качестве первого аргумента
    argc--, argv++;

    parse_files(argc, argv);

    show_parsing_result(errors_count);

    if (errors_count == 0) {
        write_output_tree(NULL);
        return EXIT_SUCCESS;
    }

    return EXIT_FAILURE;
}
