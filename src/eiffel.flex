%{
    #include <stdio.h>
    #include <stdint.h>
    #include <stdbool.h>

    #include "lex_utils.h"
    #include "strbuf.h"
%}

%option noyywrap
%option yylineno
%option never-interactive


IDENTIFIER [_a-zA-Z][_a-zA-Z0-9]*

WHITESPACE [ \n\t]+

DIGIT   [0-9]
INT_10  ({DIGIT}+_+)*{DIGIT}+

HEXIT    [0-9a-fA-F]
INT_16   0[xX]({HEXIT}+_+)*{HEXIT}+

OCTIT    [0-7]
INT_8    0[cCoO]({OCTIT}+_+)*{OCTIT}+

BINIT    [01]
INT_2    0[bB]({BINIT}+_+)*{BINIT}+

REAL_NUMBER_PART           {DIGIT}+
REAL_NUMBER                {REAL_NUMBER_PART}?\.{REAL_NUMBER_PART}|{REAL_NUMBER_PART}\.{REAL_NUMBER_PART}?
REAL_NUMBER_EXPONENT       ({REAL_NUMBER}|{REAL_NUMBER_PART})[eE][\-+]?{REAL_NUMBER_PART}


%x SINGLE_LINE_COMMENT
%x CHARACTER
%x STRING
%x VERBATIM_ALIGNED_STRING


%%

%{
    int start_line;
    int64_t int_number;
    double real_number;
    strbuf* buf = strbuf_empty();

    bool needDelimeter = false;
%}

":="					{ printf("Found operator \"%s\" in line %d\n", "ASSIGN", yylineno); }
"="						{ printf("Found operator \"%s\" in line %d\n", "EQUALS", yylineno); }
"/="					{ printf("Found operator \"%s\" in line %d\n", "NOT_EQUALS", yylineno); }
"<" 					{ printf("Found operator \"%s\" in line %d\n", "LESS", yylineno); }
"<=" 					{ printf("Found operator \"%s\" in line %d\n", "LESS_OR_EQUAL", yylineno); }
">" 					{ printf("Found operator \"%s\" in line %d\n", "GREATER", yylineno); }
">=" 					{ printf("Found operator \"%s\" in line %d\n", "GREATER_OR_EQUAL", yylineno); }
"and" 					{ printf("Found operator \"%s\" in line %d\n", "AND", yylineno); }
"xor" 					{ printf("Found operator \"%s\" in line %d\n", "XOR", yylineno); }
"or" 					{ printf("Found operator \"%s\" in line %d\n", "OR", yylineno); }
"not" 					{ printf("Found operator \"%s\" in line %d\n", "NOT", yylineno); }
and{WHITESPACE}then 	{ printf("Found operator \"%s\" in line %d\n", "AND_THEN", yylineno); }
or{WHITESPACE}else 	    { printf("Found operator \"%s\" in line %d\n", "OR_ELSE", yylineno); }
"implies" 				{ printf("Found operator \"%s\" in line %d\n", "IMPLIES", yylineno); }
"//"					{ printf("Found operator \"%s\" in line %d\n", "DIV", yylineno); }
\\\\					{ printf("Found operator \"%s\" in line %d\n", "MOD", yylineno); }
"+" 					{ printf("Found operator \"%s\" in line %d\n", yytext, yylineno); }
"-" 					{ printf("Found operator \"%s\" in line %d\n", yytext, yylineno); }
"*" 					{ printf("Found operator \"%s\" in line %d\n", yytext, yylineno); }
"/"						{ printf("Found operator \"%s\" in line %d\n", yytext, yylineno); }
"^" 					{ printf("Found operator \"%s\" in line %d\n", yytext, yylineno); }
";" 					{ printf("Found operator \"%s\" in line %d\n", yytext, yylineno); }

"(" 					{ printf("Found symbol \"%s\" in line %d\n", yytext, yylineno); }
")" 					{ printf("Found symbol \"%s\" in line %d\n", yytext, yylineno); }
"{" 					{ printf("Found symbol \"%s\" in line %d\n", yytext, yylineno); }
"}" 					{ printf("Found symbol \"%s\" in line %d\n", yytext, yylineno); }
"[" 					{ printf("Found symbol \"%s\" in line %d\n", yytext, yylineno); }
"]" 					{ printf("Found symbol \"%s\" in line %d\n", yytext, yylineno); }
":" 					{ printf("Found symbol \"%s\" in line %d\n", yytext, yylineno); }
"." 					{ printf("Found symbol \"%s\" in line %d\n", yytext, yylineno); }
"," 					{ printf("Found symbol \"%s\" in line %d\n", yytext, yylineno); }

"all" 					{ printf("Found keyword \"%s\" in line %d\n", "ALL", yylineno); }
"across"                { printf("Found keyword \"%s\" in line %d\n", "ACROSS", yylineno); }
"agent"                 { printf("Found keyword \"%s\" in line %d\n", "AGENT", yylineno); }
"alias"                 { printf("Found keyword \"%s\" in line %d\n", "ALIAS", yylineno); }
"as"                    { printf("Found keyword \"%s\" in line %d\n", "AS", yylineno); }
"assign"                { printf("Found keyword \"%s\" in line %d\n", "ASSING", yylineno); }
"attribute"             { printf("Found keyword \"%s\" in line %d\n", "ATTRIBUTE", yylineno); }
"class" 				{ printf("Found keyword \"%s\" in line %d\n", "CLASS", yylineno); }
"check"                 { printf("Found keyword \"%s\" in line %d\n", "CHECK", yylineno); }
"convert"               { printf("Found keyword \"%s\" in line %d\n", "CONVERT", yylineno); }
"create" 				{ printf("Found keyword \"%s\" in line %d\n", "CREATE", yylineno); }
"Current" 				{ printf("Found keyword \"%s\" in line %d\n", "CURRENT", yylineno); }
"do" 					{ printf("Found keyword \"%s\" in line %d\n", "DO", yylineno); }
"debug"                 { printf("Found keyword \"%s\" in line %d\n", "DEBUG", yylineno); }
"deferred"              { printf("Found keyword \"%s\" in line %d\n", "DEFERRED", yylineno); }
"else" 					{ printf("Found keyword \"%s\" in line %d\n", "ELSE", yylineno); }
"elseif" 				{ printf("Found keyword \"%s\" in line %d\n", "ELSEIF", yylineno); }
"end" 					{ printf("Found keyword \"%s\" in line %d\n", "END", yylineno); }
"ensure"                { printf("Found keyword \"%s\" in line %d\n", "ENSURE", yylineno); }
"expanded"              { printf("Found keyword \"%s\" in line %d\n", "EXPANDED", yylineno); }
"export"                { printf("Found keyword \"%s\" in line %d\n", "EXPORT", yylineno); }
"external"              { printf("Found keyword \"%s\" in line %d\n", "EXTERNAL", yylineno); }
"feature" 				{ printf("Found keyword \"%s\" in line %d\n", "FEATURE", yylineno); }
"from" 					{ printf("Found keyword \"%s\" in line %d\n", "FROM", yylineno); }
"False"                 { printf("Found keyword \"%s\" in line %d\n", "FALSE", yylineno); }
"frozen"                { printf("Found keyword \"%s\" in line %d\n", "FROZEN", yylineno); }
"if" 					{ printf("Found keyword \"%s\" in line %d\n", "IF", yylineno); }
"inherit" 				{ printf("Found keyword \"%s\" in line %d\n", "INHERIT", yylineno); }
"inspect"               { printf("Found keyword \"%s\" in line %d\n", "INSPECT", yylineno); }
"invariant"             { printf("Found keyword \"%s\" in line %d\n", "INVARIANT", yylineno); }
"local" 				{ printf("Found keyword \"%s\" in line %d\n", "LOCAL", yylineno); }
"loop" 					{ printf("Found keyword \"%s\" in line %d\n", "LOOP", yylineno); }
"like"                  { printf("Found keyword \"%s\" in line %d\n", "LIKE", yylineno); }
"note" 					{ printf("Found keyword \"%s\" in line %d\n", "NOTE", yylineno); }
"obsolete"              { printf("Found keyword \"%s\" in line %d\n", "OBSOLETE", yylineno); }
"old"                   { printf("Found keyword \"%s\" in line %d\n", "OLD", yylineno); }
"once"                  { printf("Found keyword \"%s\" in line %d\n", "ONCE", yylineno); }
"only"                  { printf("Found keyword \"%s\" in line %d\n", "ONLY", yylineno); }
"Precursor" 			{ printf("Found keyword \"%s\" in line %d\n", "PRECURSOR", yylineno); }
"redefine" 				{ printf("Found keyword \"%s\" in line %d\n", "REDEFINE", yylineno); }
"rename" 				{ printf("Found keyword \"%s\" in line %d\n", "RENAME", yylineno); }
"Result" 				{ printf("Found keyword \"%s\" in line %d\n", "RESULT", yylineno); }
"require"               { printf("Found keyword \"%s\" in line %d\n", "REQUIRE", yylineno); }
"rescue"                { printf("Found keyword \"%s\" in line %d\n", "RESCUE", yylineno); }
"retry"                 { printf("Found keyword \"%s\" in line %d\n", "RETRY", yylineno); }
"separate"              { printf("Found keyword \"%s\" in line %d\n", "SEPARATE", yylineno); }
"select" 				{ printf("Found keyword \"%s\" in line %d\n", "SELECT", yylineno); }
"then" 					{ printf("Found keyword \"%s\" in line %d\n", "THEN", yylineno); }
"True"                  { printf("Found keyword \"%s\" in line %d\n", "TRUE", yylineno); }
"undefine" 				{ printf("Found keyword \"%s\" in line %d\n", "UNDEFINE", yylineno); }
"until" 				{ printf("Found keyword \"%s\" in line %d\n", "UNTIL", yylineno); }
"variant"               { printf("Found keyword \"%s\" in line %d\n", "VARIANT", yylineno); }
"Void"                  { printf("Found keyword \"%s\" in line %d\n", "VOID", yylineno); }
"when"                  { printf("Found keyword \"%s\" in line %d\n", "WHEN", yylineno); }

"ARRAY" 				{ printf("Found keyword \"%s\" in line %d\n", "ARRAY", yylineno); }
"INTEGER" 				{ printf("Found keyword \"%s\" in line %d\n", "INTEGER", yylineno); }
"REAL" 					{ printf("Found keyword \"%s\" in line %d\n", "REAL", yylineno); }
"CHARACTER" 			{ printf("Found keyword \"%s\" in line %d\n", "CHARACTER", yylineno); }
"STRING" 				{ printf("Found keyword \"%s\" in line %d\n", "STRING", yylineno); }
"TUPLE"                 { printf("Found keyword \"%s\" in line %d\n", "TUPLE", yylineno); }
"BOOLEAN" 				{ printf("Found keyword \"%s\" in line %d\n", "BOOLEAN", yylineno); }


--                      { printf("Line %d: comment start\n", yylineno); BEGIN(SINGLE_LINE_COMMENT); }

<SINGLE_LINE_COMMENT>.* { printf("Line %d: comment: %s\n", yylineno, yytext); }

<SINGLE_LINE_COMMENT>\n { printf("Line %d: single line comment end\n", yylineno); BEGIN(INITIAL); }


<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%\/[0-9]{1,3}\/ {
    printf("Line %d: character decimal encoded\n", yylineno);
    strbuf_append_char(buf, convert_decimal_encoded_char(yytext));
}
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%%      { strbuf_append_char(buf, '%'); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%[nN]   { strbuf_append_char(buf, '\n'); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%[tT]   { strbuf_append_char(buf, '\t'); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%[aA]   { strbuf_append_char(buf, '@'); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%[bB]   { strbuf_append_char(buf, '\b'); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%[cC]   { strbuf_append_char(buf, '^'); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%[dD]   { strbuf_append_char(buf, '$'); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%[fF]   { strbuf_append_char(buf, '\f'); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%[hH]   { strbuf_append_char(buf, '\\'); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%[lL]   { strbuf_append_char(buf, '~'); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%[qQ]   { strbuf_append_char(buf, '`'); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%[rR]   { strbuf_append_char(buf, '\r'); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%[sS]   { strbuf_append_char(buf, '#'); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%[uU]   { strbuf_append_char(buf, '\0'); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%[vV]   { strbuf_append_char(buf, '\v'); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%\(     { strbuf_append_char(buf, '['); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%\)     { strbuf_append_char(buf, ']'); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%\<     { strbuf_append_char(buf, '{'); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%\>     { strbuf_append_char(buf, '}'); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%\"     { strbuf_append_char(buf, '\"'); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%\'     { strbuf_append_char(buf, '\''); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%(.|\n) { printf("Line %d: ERROR: invalid escape sequence\n", yylineno); }

<CHARACTER>[^\'\n]* { strbuf_append(buf, yytext); }

<CHARACTER>\n       { printf("Line %d: ERROR: unclosed character\n", yylineno); return -1; }

<CHARACTER><<EOF>>  { printf("Line %d: ERROR: unclosed character\n", yylineno); return -1; }

<CHARACTER>\' {
    if (buf->size == 0) {
        printf("Line %d: ERROR: empty characters are not permitted\n", yylineno);
    }
    else if (buf->size > 1) {
        printf(
            "Line %d: ERROR: expected only one character in single quotes, but got \"%s\"\n",
            yylineno,
            buf->size,
            buf->buffer
        );
    }
    else {
        printf("Line %d: found character: '%c'\n", yylineno, buf->buffer[0]);
    }
    BEGIN(INITIAL);
}

<STRING>[^\"\n%]*   { printf("Line %d: part of string\n", yylineno); strbuf_append(buf, yytext); }

<STRING>\n          { printf("Line %d: ERROR: unclosed string\n", yylineno); return -1; }

<STRING><<EOF>>     { printf("Line %d: ERROR: unclosed string\n", yylineno); return -1; }

<STRING>\" {
    printf("Line %d: string content: %s\n", yylineno, buf->buffer);\
    needDelimeter = true;
    BEGIN(INITIAL);
}

\"\[\n? {
    start_line = yylineno;
    strbuf_clear(buf);
    BEGIN(VERBATIM_ALIGNED_STRING);
}

<VERBATIM_ALIGNED_STRING>\]\" {
    printf("Found verbatim string at %d to %d line.\n", start_line, yylineno);
    printf("Verbatim string:\n");
    puts(buf->buffer);
    needDelimeter = true;
    BEGIN(INITIAL);
}

<VERBATIM_ALIGNED_STRING>([^\]%]*\n?)* { strbuf_append(buf, yytext); }

<VERBATIM_ALIGNED_STRING>\]            { strbuf_append_char(buf, ']'); }

<VERBATIM_ALIGNED_STRING><<EOF>>       { printf("Line %d: ERROR: verbatium aligned string unclosed", yylineno); return -1; }

\" {
    printf("Line %d: string start\n", yylineno);
    strbuf_clear(buf);
    BEGIN(STRING);
}

\' {
    printf("Line %d: character start\n", yylineno);
    strbuf_clear(buf);
    BEGIN(CHARACTER);
}


{IDENTIFIER} {
    if (needDelimeter) {
        printf("Line %d: invalid number literal\n", yylineno);
    }
    else {
        strbuf_clear(buf);
        strbuf_append(buf, yytext);
        printf("Line %d: found identifier: %s\n", yylineno, buf->buffer);
    }
    needDelimeter = false;
}

{INT_10} {
    parse_integer(&int_number, yytext, 10);
    printf("Line %d: found decimal number: %d\n", yylineno, int_number);
    needDelimeter = true;
}

{INT_16} {
    parse_integer(&int_number, yytext, 16);
    printf("Line %d: found hex number: %d\n", yylineno, int_number);
    needDelimeter = true;
}

{INT_8} {
    parse_integer(&int_number, yytext, 8);
    printf("Line %d: found oct number: %d\n", yylineno, int_number);
    needDelimeter = true;
}

{INT_2} {
    parse_integer(&int_number, yytext, 2);
    printf("Line %d: found bin number: %d\n", yylineno, int_number);
    needDelimeter = true;
}

{REAL_NUMBER} {
    parse_real(&real_number, yytext);
    printf("Line %d: found real number: %f\n", yylineno, real_number);
    needDelimeter = true;
}

{REAL_NUMBER_EXPONENT} {
    parse_real(&real_number, yytext);
    printf("Line %d: found real exponent number: %f\n", yylineno, real_number);
    needDelimeter = true;
}

{WHITESPACE} {
    needDelimeter = false;
}


. { printf("Line %d: found unknown symbol\n", yylineno); }


%%


int main(void) {
    yylex();
}
