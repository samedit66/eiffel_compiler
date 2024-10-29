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
    struct Expr *expr;
}

%token <int_num> INTC
%token <real_num> REALC

%type <expr> expr

%left '+' '-'


%%

expr: INTC          { $$ = Expr_int_const($1); }
    | REALC         { $$ = Expr_real_const($1); }
    | expr '+' expr { $$ = Expr_add_op($1, $3); result = $$; }
    | expr '-' expr { $$ = Expr_sub_op($1, $3); result = $$; }

%%


int main(int argc, char **argv) {
    yyparse();
    print_tree(result);
    return 0;
}
