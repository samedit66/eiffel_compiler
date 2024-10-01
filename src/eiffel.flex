%{
    #include <stdio.h>
%}

%option noyywrap
%option yylineno
%option case-insensitive
%option never-interactive

IDENTIFIER [_a-zA-Z][_a-zA-Z0-9]*

WHITESPACE [ \n\t]+

DIGIT          [0-9]
DECIMAL_NUMBER ({DIGIT}+_)*{DIGIT}+

HEXIT          [0-9a-fA-F]
HEX_NUMBER     0[xX]({HEXIT}+_)*{HEXIT}+

OCTIT          [0-7]
OCT_NUMBER     0[cCoO]({OCTIT}+_)*{OCTIT}+

BINIT          [01]
BIN_NUMBER     0[bB]({BINIT}+_)*{BINIT}+

REAL_NUMBER                {DECIMAL_NUMBER}\.|\.{DECIMAL_NUMBER}|{DECIMAL_NUMBER}\.{DECIMAL_NUMBER}
REAL_NUMBER_EXPONENT       {REAL_NUMBER}[eE][\-+]?{DECIMAL_NUMBER}


%x SINGLE_LINE_COMMENT
%x CHARACTER
%x STRING


%%

class { printf("Line %d: found keyword class", yylineno); } /* Ключевые слова начинаются тут */


--                      { printf("Line %d: comment start\n", yylineno); BEGIN(SINGLE_LINE_COMMENT); }

<SINGLE_LINE_COMMENT>.* { printf("Line %d: comment: %s\n", yylineno, yytext); }

<SINGLE_LINE_COMMENT>\n { printf("Line %d: single line comment end\n", yylineno); BEGIN(INITIAL); }


\"                                 { printf("Line %d: string start\n", yylineno); BEGIN(STRING); }

\'                                 { printf("Line %d: character start\n", yylineno); BEGIN(CHARACTER); }

<CHARACTER,STRING>%\/[0-9]{1,3}\/% { printf("Line %d: character decimal encoded\n", yylineno); }
<CHARACTER,STRING>%%               { printf("Line %d: percent character\n", yylineno); }
<CHARACTER,STRING>%[nN]            { printf("Line %d: newline character\n", yylineno); }
<CHARACTER,STRING>%[tT]            { printf("Line %d: horizontal tab character\n", yylineno); }
<CHARACTER,STRING>%[aA]            { printf("Line %d: at sign character\n", yylineno); }
<CHARACTER,STRING>%[bB]            { printf("Line %d: backspace character\n", yylineno); }
<CHARACTER,STRING>%[cC]            { printf("Line %d: circumflex character\n", yylineno); }
<CHARACTER,STRING>%[dD]            { printf("Line %d: dollar character\n", yylineno); }
<CHARACTER,STRING>%[fF]            { printf("Line %d: form feed character\n", yylineno); }
<CHARACTER,STRING>%[hH]            { printf("Line %d: backslash character\n", yylineno); }
<CHARACTER,STRING>%[lL]            { printf("Line %d: tilde character\n", yylineno); }
<CHARACTER,STRING>%[qQ]            { printf("Line %d: backquote character\n", yylineno); }
<CHARACTER,STRING>%[rR]            { printf("Line %d: carriage return character\n", yylineno); }
<CHARACTER,STRING>%[sS]            { printf("Line %d: sharp character\n", yylineno); }
<CHARACTER,STRING>%[uU]            { printf("Line %d: null character\n", yylineno); }
<CHARACTER,STRING>%[vV]            { printf("Line %d: vertical bar character\n", yylineno); }
<CHARACTER,STRING>%\(              { printf("Line %d: opening bracket character\n", yylineno); }
<CHARACTER,STRING>%\)              { printf("Line %d: closing bracket character\n", yylineno); }
<CHARACTER,STRING>%\<              { printf("Line %d: opening brace character\n", yylineno); }
<CHARACTER,STRING>%\>              { printf("Line %d: closingg brace character\n", yylineno); }
<CHARACTER,STRING>%\"              { printf("Line %d: double quote character\n", yylineno); }
<CHARACTER,STRING>%\'              { printf("Line %d: single quote character\n", yylineno); }
<CHARACTER,STRING>%.               { printf("Line %d: ERROR: invalid escape sequence\n", yylineno); return -1; }
<CHARACTER>[^\'\n]+                { printf("Line %d: character content: %s\n", yylineno, yytext); }

<CHARACTER>\n                      { printf("Line %d: ERROR: unclosed character\n", yylineno); return -1; }

<CHARACTER><<EOF>>                 { printf("Line %d: ERROR: unclosed character\n", yylineno); return -1; }

<CHARACTER>\'                      { printf("Line %d: character end\n", yylineno); BEGIN(INITIAL); }

<STRING>[^\"\n]                    { printf("Line %d: part of string\n", yylineno); }

<STRING>\n                         { printf("Line %d: ERROR: unclosed string\n", yylineno); return -1; }

<STRING><<EOF>>                    { printf("Line %d: ERROR: unclosed string\n", yylineno); return -1; }

<STRING>\"                         { printf("Line %d: string end\n", yylineno); BEGIN(INITIAL); }


{IDENTIFIER}     { printf("Line %d: found identifier: %s\n", yylineno, yytext); }

{DECIMAL_NUMBER} { printf("Line %d: found decimal number: %s\n", yylineno, yytext); }

{HEX_NUMBER}     { printf("Line %d: found hex number: %s\n", yylineno, yytext); }

{OCT_NUMBER}     { printf("Line %d: found oct number: %s\n", yylineno, yytext); }

{BIN_NUMBER}     { printf("Line %d: found bin number: %s\n", yylineno, yytext); }

{REAL_NUMBER}    { printf("Line %d: found real number: %s\n", yylineno, yytext); }

{REAL_NUMBER_EXPONENT} { printf("Line %d: found real exponent number: %s\n", yylineno, yytext); }

{WHITESPACE}     { printf("Line %d: found whitespace\n", yylineno); }


.                { printf("Line %d: found unknown symbol\n", yylineno); }

%%

int main(void) {
    yylex();
}
