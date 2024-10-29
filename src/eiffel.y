%{
    #include <stdio.h>
    #include <stdlib.h>

    extern int yylex(void);

    void yyerror(const char *str) {
        fprintf(stderr, "error: %s\n", str);
    }
%}

%union {
    int int_num;
    double real_num;
}

%token <int_num>  INTC
%token <real_num> REALC

%%

explist: /* nothing */
       | explist exp

exp: INTC  { printf("%d\n", $1); }
   | REALC { printf("%f\n", $1); }

%%

int main(int argc, char **argv) {
    yyparse();
    return 0;
}
