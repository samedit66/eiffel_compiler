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
    | ';'
    ;


assign_stmt: expr ASSIGN_TO expr %prec LOWER_THAN_EXPR { LOG_NODE("assign_stmt"); }
           ;


loop_stmt: FROM stmt_list_opt UNTIL expr LOOP stmt_list_opt END
         ;


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


if_stmt: IF expr THEN stmt_list_opt END { LOG_NODE("if"); }
       | IF expr THEN stmt_list_opt else_clause END { LOG_NODE("if-else"); }
       ;

else_clause: ELSE stmt_list_opt
           | elseif_clauses
           ;

elseif_clauses: ELSEIF expr THEN stmt_list_opt
              | ELSEIF expr THEN stmt_list_opt else_clause
              ;


literal: INT_CONST  
       | REAL_CONST 
       | IDENT_LIT  
       | CHAR_CONST

expr: literal              
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
    ;
%%

int main(int argc, char **argv) {
    yyparse();
    return 0;
}
