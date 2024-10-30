%{
    #include <stdio.h>
    #include <stdlib.h>

    #include "./include/ast.h"

    extern int yylex(void);

    void yyerror(const char *str) {
        fprintf(stderr, "error: %s\n", str);
    }

    Expr *result = NULL;
%}


%union {
    int int_num;
    double real_num;
    char *name;
    char *str;
    struct Expr *expr;
}

%token <int_num> INTC
%token <real_num> REALC
%token <name> NAME_LIT

%token INT_DIV MOD
%token AND OR NOT AND_THEN OR_ELSE
%token NEQ LE GE

%type <expr> expr root

%right IMPLIES
%left OR OR_ELSE XOR
%left AND AND_THEN
%right NOT
%left '<' '>' LE GE '=' NEQ
%left '+' '-'
%left '*' '/' INT_DIV MOD
%right '^'

%%

root: expr { $$ = $1; result = $$; }

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
%%


int main(int argc, char **argv) {
    yyparse();
    print_tree(result);
    return 0;
}
