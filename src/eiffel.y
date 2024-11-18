%{
    #include <stdio.h>
    #include <stdlib.h>

    extern int yylex(void);
    extern void yyrestart(FILE *infile);

    void yyerror(const char *str) {
        fprintf(stderr, "error: %s\n", str);
    }

    #define YYDEBUG 1

    #define LOG_NODE(msg) printf("Found node: %s\n", msg)
%}

%define parse.error verbose

%union {
    int int_num;
    double real_num;
    char *name;
    char *str;
}

%start program

%token EOI 0 "end of file"

%token <int_num>  INT_CONST
%token <real_num> REAL_CONST
%token <name>     IDENT_LIT 
%token <int_num>  CHAR_CONST
%token <str>      STRING_CONST

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

%type <stmt> stmt assign_stmt if_stmt loop_stmt
%type <expr> expr constant

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
assign_stmt: writable ASSIGN_TO expr { LOG_NODE("assign_stmt"); }
           ;

writable: IDENT_LIT
        | RESULT
        | bracket_access
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
call: simple_call
    | precursor_call
    | RESULT         '.' simple_call
    | CURRENT        '.' simple_call
    | '(' expr ')'   '.' simple_call
    | bracket_access '.' simple_call
    | call           '.' simple_call
    ;

precursor_call: PRECURSOR %prec LOWER_THAN_EXPR
              | PRECURSOR '(' params_list ')'
              ;

simple_call: IDENT_LIT %prec LOWER_THAN_PARENS
           | IDENT_LIT '(' params_list ')'
           ;

params_list: /* empty */
           | comma_separated_exprs
           ;

comma_separated_exprs: expr
                     | comma_separated_exprs ',' expr
                     ;


/* ********************************************************************/
/* Тернарный оператор */
if_expr: IF expr THEN expr elseif_expr_opt ELSE expr END

elseif_expr_opt: /* empty */
               | elseif_expr

elseif_expr: ELSEIF expr THEN expr
           | elseif_expr ELSEIF expr THEN expr


/* ********************************************************************/
/* Описание выражений */

/* Взятие элемента через квадратный скобки */
bracket_access: call '[' expr ']' 
              | bracket_access '[' expr ']'
              ;

/* Константы */
constant: INT_CONST  
        | REAL_CONST
        | CHAR_CONST
        | STRING_CONST
        | RESULT
        | CURRENT
        | TRUE_KW
        | FALSE_KW
        | VOID
        ;

expr: constant
    | expr '+' expr        
    | expr '-' expr        
    | expr '*' expr        
    | expr '/' expr        
    | '(' expr ')'
    | '+' expr %prec UPLUS 
    | '-' expr %prec UMINUS
    | expr INT_DIV expr    
    | expr MOD expr        
    | expr '^' expr        
    | expr AND expr        
    | expr OR expr         
    | NOT expr             
    | expr AND_THEN expr   
    | expr OR_ELSE expr    
    | expr XOR expr        
    | expr '<' expr        
    | expr '>' expr        
    | expr '=' expr        
    | expr LE expr         
    | expr GE expr         
    | expr NEQ expr        
    | expr IMPLIES expr 
    | call
    | bracket_access
    | if_expr
    ;
%%

int main(int argc, char **argv) {
    yydebug = 1;

    if (argc > 1) {
        puts("Parsing files mode on");
        for (int i = 1; i < argc; i++) {
            FILE *file = fopen(argv[i], "r");
            if (file == NULL) {
                perror(argv[i]);
                continue;
            }

            yyrestart(file);
            yyparse();
        }
        
        return 0;
    }

    puts("Parsing from user input");
    yyparse();
    return 0;
}
