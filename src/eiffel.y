%{
    #include <stdio.h>
    #include <stdlib.h>

    #include "./include/ast.h"

    extern int yylex(void);

    void yyerror(const char *str) {
        fprintf(stderr, "error: %s\n", str);
    }

    #define LOG_NODE(msg) printf("Found node: %s\n", msg)

    Stmt *result = NULL;
%}


%union {
    int int_num;
    double real_num;
    char *name;
    char *str;
    struct Expr *expr;
    struct Stmt *stmt;
}

%start program

%token EOI 0 "end of file"

%token <int_num> INTC
%token <real_num> REALC
%token <name> IDENT_LIT 

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

%type <stmt> stmt assign_stmt if_stmt loop_stmt
%type <expr> expr literal

%nonassoc LOWER_THAN_EXPR
%right IMPLIES
%left OR OR_ELSE XOR
%left AND AND_THEN
%right NOT
%left '<' '>' LE GE '=' NEQ
%left '+' '-'
%left '*' '/' INT_DIV MOD
%right '^'
%nonassoc UMINUS UPLUS

%%

program: stmt_list { LOG_NODE("program"); }
       ;


class: CLASS IDENT_LIT END { LOG_NODE("class"); }
     ;


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
    ;


assign_stmt: expr ASSIGN_TO expr %prec LOWER_THAN_EXPR { LOG_NODE("assign_stmt"); }
           ;


loop_stmt: FROM stmt_list_opt UNTIL expr LOOP stmt_list_opt END
         ;


inspect_stmt: INSPECT expr inspect_clauses_opt END

choices: expr
       | expr TWO_DOTS expr
       | choices ',' expr
       ;

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


if_stmt: IF expr THEN stmt_list_opt END { LOG_NODE("if"); }
       | IF expr THEN stmt_list_opt else_clause END { LOG_NODE("if-else"); }
       ;

else_clause: ELSE stmt_list_opt
           | elseif_clauses
           ;

elseif_clauses: ELSEIF expr THEN stmt_list_opt
              | ELSEIF expr THEN stmt_list_opt else_clause
              ;


literal: INTC      { $$ = Expr_int_const($1); }
       | REALC     { $$ = Expr_real_const($1); }
       | IDENT_LIT { $$ = Expr_ident($1); }

expr: literal               { $$ = $1; }
    | expr '+' expr         { $$ = Expr_bin_op(ADD_OP, $1, $3); }
    | expr '-' expr         { $$ = Expr_bin_op(SUB_OP, $1, $3); }
    | expr '*' expr         { $$ = Expr_bin_op(MUL_OP, $1, $3); }
    | expr '/' expr         { $$ = Expr_bin_op(DIV_OP, $1, $3); }
    | '(' expr ')'          { $$ = $2; }
    | '+' expr %prec UPLUS  { $$ = $2; }
    | '-' expr %prec UMINUS { $$ = Expr_unary_op(NEG_OP, $2); }
    | expr INT_DIV expr     { $$ = Expr_bin_op(INT_DIV_OP, $1, $3); }
    | expr MOD expr         { $$ = Expr_bin_op(MOD_OP, $1, $3); }
    | expr '^' expr         { $$ = Expr_bin_op(POW_OP, $1, $3); }
    | expr AND expr         { $$ = Expr_bin_op(AND_OP, $1, $3); }
    | expr OR expr          { $$ = Expr_bin_op(OR_OP, $1, $3); }
    | NOT expr              { $$ = Expr_unary_op(NOT_OP, $2); }
    | expr AND_THEN expr    { $$ = Expr_bin_op(AND_THEN_OP, $1, $3); }
    | expr OR_ELSE expr     { $$ = Expr_bin_op(OR_ELSE_OP, $1, $3); }
    | expr XOR expr         { $$ = Expr_bin_op(XOR_OP, $1, $3); }
    | expr '<' expr         { $$ = Expr_bin_op(LT_OP, $1, $3); LOG_NODE("less"); }
    | expr '>' expr         { $$ = Expr_bin_op(GT_OP, $1, $3); }
    | expr '=' expr         { $$ = Expr_bin_op(EQ_OP, $1, $3); }
    | expr LE expr          { $$ = Expr_bin_op(LE_OP, $1, $3); }
    | expr GE expr          { $$ = Expr_bin_op(GE_OP, $1, $3); }
    | expr NEQ expr         { $$ = Expr_bin_op(NEQ_OP, $1, $3); }
    | expr IMPLIES expr     { $$ = Expr_bin_op(IMPLIES_OP, $1, $3); }
    ;
%%

int main(int argc, char **argv) {
    yyparse();
    return 0;
}
