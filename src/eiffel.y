%{
    #include <stdio.h>
    #include <stdlib.h>

    #include "./include/ast.h"

    extern int yylex(void);

    void yyerror(const char *str) {
        fprintf(stderr, "error: %s\n", str);
    }

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

%token <int_num> INTC
%token <real_num> REALC
%token <name> NAME_LIT

%token INT_DIV MOD
%token AND OR NOT AND_THEN OR_ELSE
%token NEQ LE GE
%token ASSIGN_TO
%token END
%token IF THEN ELSEIF ELSE
%token FROM UNTIL LOOP

%type <stmt> stmt assign_stmt
%type <expr> expr
%type <expr> lvalue

%right IMPLIES
%left OR OR_ELSE XOR
%left AND AND_THEN
%right NOT
%left '<' '>' LE GE '=' NEQ
%left '+' '-'
%left '*' '/' INT_DIV MOD
%right '^'

%%

program: stmt_list_opt
       ;

stmt_list_opt: /* empty */
             | stmt_list

stmt_list: stmt
         | stmt_list stmt
         ;

stmt: assign_stmt
    | if_stmt
    | loop_stmt
    ;


loop_init: FROM stmt_list 
         ;

loop_cond: UNTIL expr
         ;

loop_prefix: loop_init
           | loop_cond
           | loop_init loop_cond
           ;

loop_stmt: loop_prefix LOOP stmt_list_opt END
         ;


if_stmt: IF expr THEN stmt_list_opt END
       | IF expr THEN stmt_list_opt else_clause END
       ;

else_clause: ELSE stmt_list_opt
           | elseif_clauses
           ;

elseif_clauses: ELSEIF expr THEN stmt_list_opt
              | ELSEIF expr THEN stmt_list_opt else_clause
              ;


lvalue: NAME_LIT { $$ = Expr_name_lit($1); }
      ;

assign_stmt: lvalue ASSIGN_TO expr { $$ = Stmt_assign_stmt($1, $3); }
           ;


expr: INTC               { $$ = Expr_int_const($1); }
    | REALC              { $$ = Expr_real_const($1); }
    | NAME_LIT           { $$ = Expr_name_lit($1); }
    | expr '+' expr      { $$ = Expr_bin_op(ADD_OP, $1, $3); }
    | expr '-' expr      { $$ = Expr_bin_op(SUB_OP, $1, $3); }
    | expr '*' expr      { $$ = Expr_bin_op(MUL_OP, $1, $3); }
    | expr '/' expr      { $$ = Expr_bin_op(DIV_OP, $1, $3); }
    | '(' expr ')'       { $$ = $2; }
    | '-' expr %prec '-' { $$ = Expr_unary_op(NEG_OP, $2); }
    | expr INT_DIV expr  { $$ = Expr_bin_op(INT_DIV_OP, $1, $3); }
    | expr MOD expr      { $$ = Expr_bin_op(MOD_OP, $1, $3); }
    | expr '^' expr      { $$ = Expr_bin_op(POW_OP, $1, $3); }
    | expr AND expr      { $$ = Expr_bin_op(AND_OP, $1, $3); }
    | expr OR expr       { $$ = Expr_bin_op(OR_OP, $1, $3); }
    | NOT expr           { $$ = Expr_unary_op(NOT_OP, $2); }
    | expr AND_THEN expr { $$ = Expr_bin_op(AND_THEN_OP, $1, $3); }
    | expr OR_ELSE expr  { $$ = Expr_bin_op(OR_ELSE_OP, $1, $3); }
    | expr XOR expr      { $$ = Expr_bin_op(XOR_OP, $1, $3); }
    | expr '<' expr      { $$ = Expr_bin_op(LT_OP, $1, $3); }
    | expr '>' expr      { $$ = Expr_bin_op(GT_OP, $1, $3); }
    | expr '=' expr      { $$ = Expr_bin_op(EQ_OP, $1, $3); }
    | expr LE expr       { $$ = Expr_bin_op(LE_OP, $1, $3); }
    | expr GE expr       { $$ = Expr_bin_op(GE_OP, $1, $3); }
    | expr NEQ expr      { $$ = Expr_bin_op(NEQ_OP, $1, $3); }
    | expr IMPLIES expr  { $$ = Expr_bin_op(IMPLIES_OP, $1, $3); }
    ;
%%


int main(int argc, char **argv) {
    yyparse();
    //print_stmt(result);
    return 0;
}
