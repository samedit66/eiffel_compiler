%{
    #include <stdio.h>
    #include <stdlib.h>

    extern int yylex(void);

    void yyerror(const char *str) {
        fprintf(stderr, "error: %s\n", str);
    }

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

%token INT_DIV MOD
%token AND OR NOT AND_THEN OR_ELSE
%token NEQ LE GE
%token ASSIGN_TO
%token END
%token IF THEN ELSEIF ELSE
%token FROM UNTIL LOOP
%token WHEN INSPECT TWO_DOTS
%token COMMA
%token CLASS
%token LIKE
%token DO
%token INTEGER REAL STRING_KW CHARACTER BOOLEAN ARRAY TUPLE
%token FEATURE CREATE
%token LOCAL
%token REQUIRE ENSURE
%token CURRENT PRECURSOR RESULT

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
%right '.'

%%

/* ********************************************************************/
/* Описание программы */
program: feature_list { LOG_NODE("program"); }
       ;


/* ********************************************************************/
/* Описание типов */
builtin_type: INTEGER
            | REAL
            | STRING_KW
            | CHARACTER
            | BOOLEAN
            ;

generic_type: '[' builtin_type ']'
            | '[' IDENT_LIT ']'
            ;

array_type: ARRAY generic_type
          ;

like_type: LIKE IDENT_LIT
         ;

type: IDENT_LIT
    | builtin_type
    | array_type
    | like_type
    ;


/* ********************************************************************/
/* Описания для полей и методов класса */
ident_list: IDENT_LIT
          | ident_list ',' IDENT_LIT

type_spec: ':' type
         ;

name_and_type: ident_list type_spec
             ;

args_list_opt: /* empty */
             | args_list

args_list: name_and_type
         | args_list ';' name_and_type

var_decl_list: name_and_type
             | var_decl_list name_and_type

var_decl_list_opt: /* empty */
                 | var_decl_list

local_part: LOCAL var_decl_list_opt

local_part_opt: /* empty */
              | local_part

condition: expr               %prec LOWER_THAN_EXPR
         | IDENT_LIT ':' expr %prec LOWER_THAN_EXPR
         ;

condition_list: condition
              | condition_list condition
              ;

require_part: REQUIRE condition_list
            ;

require_part_opt: /* empty */
                | require_part
                ;

ensure_part: ENSURE condition_list
           ;

ensure_part_opt: /* empty */
               | ensure_part
               ;

do_part: DO stmt_list_opt
       ;

routine_body: local_part_opt require_part_opt do_part ensure_part_opt END
            ;

feature: name_and_type  { LOG_NODE("attribute"); }
       | ident_list routine_body
       | name_and_type routine_body { LOG_NODE("routine with no parans"); }
       | ident_list '(' args_list_opt ')' routine_body { LOG_NODE("routine with parans"); }
       | ident_list '(' args_list_opt ')' type_spec routine_body { LOG_NODE("full routine"); }
       ;

feature_list: feature
            | feature_list feature
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
        ;


/* ********************************************************************/
/* Описание оператора цикла */
loop_stmt: FROM stmt_list_opt UNTIL expr LOOP stmt_list_opt END
         ;


/* ********************************************************************/
/* Описание оператора выбора */
inspect_stmt: INSPECT expr inspect_clauses_opt END { LOG_NODE("inspect_stmt"); }

choice: expr
      | expr TWO_DOTS expr

choices: choice
       | choices ',' choice

when_clause: WHEN choices THEN stmt_list_opt
           | WHEN THEN stmt_list_opt
           ;

inspect_clauses_opt: /* empty */
                   | inspect_clauses
                   ;

when_clauses: when_clause
            | when_clauses when_clause
            ;

inspect_clauses: when_clauses
               | when_clauses ELSE stmt_list_opt
               ;


/* ********************************************************************/
/* Описание оператора ветвления */
if_stmt: IF expr THEN stmt_list_opt END { LOG_NODE("if"); }
       | IF expr THEN stmt_list_opt else_clause END { LOG_NODE("if-else"); }
       ;

else_clause: ELSE stmt_list_opt
           | elseif_clauses
           ;

elseif_clauses: ELSEIF expr THEN stmt_list_opt
              | ELSEIF expr THEN stmt_list_opt else_clause
              ;


/* ********************************************************************/
/* Описание вызова метода */
call: simple_call
    | RESULT       '.' simple_call
    | CURRENT      '.' simple_call
    | PRECURSOR    '.' simple_call
    | '(' expr ')' '.' simple_call
    | call         '.' simple_call
    ;

simple_call: IDENT_LIT %prec LOWER_THAN_PARENS  { LOG_NODE("simple_call with no parens"); }
           | IDENT_LIT '(' params_list_opt ')' { LOG_NODE("simple_call with parens"); }
           ;

params_list_opt: /* empty */
               | params_list
               ;

params_list: expr
           | params_list ',' expr
           ;


/* ********************************************************************/
/* Описание выражений */
constant: INT_CONST  
        | REAL_CONST
        | CHAR_CONST
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
    ;
%%

int main(int argc, char **argv) {
    yyparse();
    return 0;
}
