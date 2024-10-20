%{
    #include <ctype.h>
    #include <stdio.h>
    #include <stdint.h>
    #include <stdbool.h>
    #include <string.h>
    #include <ctype.h>

    #include "lex_utils.h"
    #include "strbuf.h"
    #include "strlist.h"

    // Возможно, это не лучшая практика...
    #ifdef DEBUG_LEXER
        #define LOG_F(lineno, msg, ...) {\
            printf("Line %d: ", lineno);\
            printf(msg, __VA_ARGS__);\
        }
    #else
        #define LOG_F(lineno, msg, ...)
    #endif

    #define LOG_LEXEM_AT_LINENO(lineno, lexem_type, lexem)\
        LOG_F(lineno, "found %s: \"%s\"\n", lexem_type, lexem)

    #define LOG_LEXEM(lexem_type, lexem)\
        LOG_LEXEM_AT_LINENO(yylineno, lexem_type, lexem)

    #ifdef COLORFUL
        #define RED_TEXT "\033[31m%s\033[0m"
        #define UNDERSCORED_TEXT "\033[4m%s\033[0m"
    #else
        #define RED_TEXT "%s"
        #define UNDERSCORED_TEXT "%s"
    #endif
    
    #define ERROR_F(lineno, msg, ...) {\
        printf("Line %d: " RED_TEXT ": ", lineno, "error");\
        printf(msg, __VA_ARGS__);\
        printf("\n");\
    }

    #define ERROR_AT_LINENO(lineno, msg)\
        printf("Line %d: " RED_TEXT ": %s", lineno, "error", msg)

    #define ERROR(msg) ERROR_AT_LINENO(yylineno, msg)
%}

%option noyywrap
%option yylineno
%option never-interactive


IDENTIFIER [_a-zA-Z][_a-zA-sZ0-9]*

WHITESPACE [ \n\t\r]+

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
    int64_t int_number;
    double real_number;
    strbuf *buf = strbuf_empty();
    strlist *verbatim_str = strlist_new();
%}

":="					{ LOG_LEXEM("operator", ":="); }
"="						{ LOG_LEXEM("operator", "EQUALS"); }
"/="					{ LOG_LEXEM("operator", "NOT_EQUALS"); }
"<" 					{ LOG_LEXEM("operator", "LESS"); }
"<=" 					{ LOG_LEXEM("operator", "LESS_OR_EQUAL"); }
">" 					{ LOG_LEXEM("operator", "GREATER"); }
">=" 					{ LOG_LEXEM("operator", "GREATER_OR_EQUAL"); }
"and" 					{ LOG_LEXEM("operator", "AND"); }
"xor" 					{ LOG_LEXEM("operator", "XOR"); }
"or" 					{ LOG_LEXEM("operator", "OR"); }
"not" 					{ LOG_LEXEM("operator", "NOT"); }
and{WHITESPACE}then 	{ LOG_LEXEM("operator", "AND_THEN"); }
or{WHITESPACE}else 	    { LOG_LEXEM("operator", "OR_ELSE"); }
"implies" 				{ LOG_LEXEM("operator", "IMPLIES"); }
"//"					{ LOG_LEXEM("operator", "DIV"); }
"\\\\"					{ LOG_LEXEM("operator", "MOD"); }
"+" 					{ LOG_LEXEM("operator", "+"); }
"-" 					{ LOG_LEXEM("operator", "-"); }
"*" 					{ LOG_LEXEM("operator", "*"); }
"/"						{ LOG_LEXEM("operator", "/"); }
"^" 					{ LOG_LEXEM("operator", "^"); }
";" 					{ LOG_LEXEM("operator", ";"); }

"->"                    { LOG_LEXEM("symbol", "->"); }
"<<"                    { LOG_LEXEM("symbol", "<<"); }
">>"                    { LOG_LEXEM("symbol", ">>"); }
"(" 					{ LOG_LEXEM("symbol", "("); }
")" 					{ LOG_LEXEM("symbol", ")"); }
"{" 					{ LOG_LEXEM("symbol", "{"); }
"}" 					{ LOG_LEXEM("symbol", "}"); }
"[" 					{ LOG_LEXEM("symbol", "["); }
"]" 					{ LOG_LEXEM("symbol", "]"); }
":" 					{ LOG_LEXEM("symbol", ":"); }
"." 					{ LOG_LEXEM("symbol", "."); }
"," 					{ LOG_LEXEM("symbol", ","); }

"all" 					{ LOG_LEXEM("keyword", "ALL"); }
"across"                { LOG_LEXEM("keyword", "ACROSS"); }
"agent"                 { LOG_LEXEM("keyword", "AGENT"); }
"alias"                 { LOG_LEXEM("keyword", "ALIAS"); }
"as"                    { LOG_LEXEM("keyword", "AS"); }
"assign"                { LOG_LEXEM("keyword", "ASSIGN"); }
"attribute"             { LOG_LEXEM("keyword", "ATTRIBUTE"); }
"class" 				{ LOG_LEXEM("keyword", "CLASS"); }
"check"                 { LOG_LEXEM("keyword", "CHECK"); }
"convert"               { LOG_LEXEM("keyword", "CONVERT"); }
"create" 				{ LOG_LEXEM("keyword", "CREATE"); }
"Current" 				{ LOG_LEXEM("keyword", "CURRENT"); }
"do" 					{ LOG_LEXEM("keyword", "DO"); }
"debug"                 { LOG_LEXEM("keyword", "DEBUG"); }
"deferred"              { LOG_LEXEM("keyword", "DEFERRED"); }
"else" 					{ LOG_LEXEM("keyword", "ELSE"); }
"elseif" 				{ LOG_LEXEM("keyword", "ELSEIF"); }
"end" 					{ LOG_LEXEM("keyword", "END"); }
"ensure"                { LOG_LEXEM("keyword", "ENSURE"); }
"expanded"              { LOG_LEXEM("keyword", "EXPANDED"); }
"export"                { LOG_LEXEM("keyword", "EXPORT"); }
"external"              { LOG_LEXEM("keyword", "EXTERNAL"); }
"feature" 				{ LOG_LEXEM("keyword", "FEATURE"); }
"from" 					{ LOG_LEXEM("keyword", "FROM"); }
"False"                 { LOG_LEXEM("keyword", "FALSE"); }
"frozen"                { LOG_LEXEM("keyword", "FROZEN"); }
"if" 					{ LOG_LEXEM("keyword", "IF"); }
"inherit" 				{ LOG_LEXEM("keyword", "INHERIT"); }
"inspect"               { LOG_LEXEM("keyword", "INSPECT"); }
"invariant"             { LOG_LEXEM("keyword", "INVARIANT"); }
"local" 				{ LOG_LEXEM("keyword", "LOCAL"); }
"loop" 					{ LOG_LEXEM("keyword", "LOOP"); }
"like"                  { LOG_LEXEM("keyword", "LIKE"); }
"note" 					{ LOG_LEXEM("keyword", "NOTE"); }
"obsolete"              { LOG_LEXEM("keyword", "OBSOLETE"); }
"old"                   { LOG_LEXEM("keyword", "OLD"); }
"once"                  { LOG_LEXEM("keyword", "ONCE"); }
"only"                  { LOG_LEXEM("keyword", "ONLY"); }
"Precursor" 			{ LOG_LEXEM("keyword", "PRECURSOR"); }
"redefine" 				{ LOG_LEXEM("keyword", "REDEFINE"); }
"rename" 				{ LOG_LEXEM("keyword", "RENAME"); }
"Result" 				{ LOG_LEXEM("keyword", "RESULT"); }
"require"               { LOG_LEXEM("keyword", "REQUIRE"); }
"rescue"                { LOG_LEXEM("keyword", "RESCUE"); }
"retry"                 { LOG_LEXEM("keyword", "RETRY"); }
"separate"              { LOG_LEXEM("keyword", "SEPARATE"); }
"select" 				{ LOG_LEXEM("keyword", "SELECT"); }
"then" 					{ LOG_LEXEM("keyword", "THEN"); }
"True"                  { LOG_LEXEM("keyword", "TRUE"); }
"undefine" 				{ LOG_LEXEM("keyword", "UNDEFINE"); }
"until" 				{ LOG_LEXEM("keyword", "UNTIL"); }
"variant"               { LOG_LEXEM("keyword", "VARIANT"); }
"Void"                  { LOG_LEXEM("keyword", "VOID"); }
"when"                  { LOG_LEXEM("keyword", "WHEN"); }

"ARRAY" 				{ LOG_LEXEM("keyword", "ARRAY"); }
"INTEGER" 				{ LOG_LEXEM("keyword", "INTEGER"); }
"REAL" 					{ LOG_LEXEM("keyword", "REAL"); }
"CHARACTER" 			{ LOG_LEXEM("keyword", "CHARACTER"); }
"STRING" 				{ LOG_LEXEM("keyword", "STRING"); }
"TUPLE"                 { LOG_LEXEM("keyword", "TUPLE"); }
"BOOLEAN" 				{ LOG_LEXEM("keyword", "BOOLEAN"); }


--                      { BEGIN(SINGLE_LINE_COMMENT); }

<SINGLE_LINE_COMMENT>.* {
    strbuf_clear(buf);
    strbuf_append(buf, yytext);
}

<SINGLE_LINE_COMMENT>\n      { LOG_LEXEM_AT_LINENO(yylineno-1, "single line comment", buf->buffer); BEGIN(INITIAL); }
<SINGLE_LINE_COMMENT><<EOF>> { LOG_LEXEM("single line comment", buf->buffer); BEGIN(INITIAL); }

<CHARACTER,STRING>%\/[0-9]{1,3}\/ {
    strbuf_append_char(buf, convert_decimal_encoded_char(yytext));
}
<CHARACTER,STRING>%%      { strbuf_append_char(buf, '%'); }
<CHARACTER,STRING>%[nN]   { strbuf_append_char(buf, '\n'); }
<CHARACTER,STRING>%[tT]   { strbuf_append_char(buf, '\t'); }
<CHARACTER,STRING>%[aA]   { strbuf_append_char(buf, '@'); }
<CHARACTER,STRING>%[bB]   { strbuf_append_char(buf, '\b'); }
<CHARACTER,STRING>%[cC]   { strbuf_append_char(buf, '^'); }
<CHARACTER,STRING>%[dD]   { strbuf_append_char(buf, '$'); }
<CHARACTER,STRING>%[fF]   { strbuf_append_char(buf, '\f'); }
<CHARACTER,STRING>%[hH]   { strbuf_append_char(buf, '\\'); }
<CHARACTER,STRING>%[lL]   { strbuf_append_char(buf, '~'); }
<CHARACTER,STRING>%[qQ]   { strbuf_append_char(buf, '`'); }
<CHARACTER,STRING>%[rR]   { strbuf_append_char(buf, '\r'); }
<CHARACTER,STRING>%[sS]   { strbuf_append_char(buf, '#'); }
<CHARACTER,STRING>%[uU]   { strbuf_append_char(buf, '\0'); }
<CHARACTER,STRING>%[vV]   { strbuf_append_char(buf, '\v'); }
<CHARACTER,STRING>%\(     { strbuf_append_char(buf, '['); }
<CHARACTER,STRING>%\)     { strbuf_append_char(buf, ']'); }
<CHARACTER,STRING>%\<     { strbuf_append_char(buf, '{'); }
<CHARACTER,STRING>%\>     { strbuf_append_char(buf, '}'); }
<CHARACTER,STRING>%\"     { strbuf_append_char(buf, '\"'); }
<CHARACTER,STRING>%\'     { strbuf_append_char(buf, '\''); }
<CHARACTER,STRING>%(.|\n) { ERROR("invalid escape sequence"); }

<CHARACTER>[^\'\n]* {
    strbuf_append(buf, yytext);
    
    if (buf->size > 1) {
        ERROR_F(yylineno, "expected only one character in singles quotes, but got: '%s'", buf->buffer);
        return -1;
    }
}

<CHARACTER>\n       { ERROR_AT_LINENO(yylineno-1, "unclosed character literal"); return -1; }
<CHARACTER><<EOF>>  { ERROR("unclosed character literal"); return -1; }

<CHARACTER>\' {
    if (buf->size == 0) {
        ERROR("empty characters are not permitted");
    }
    else if (buf->size > 1) {
        ERROR_F(yylineno, "expected only one character in singles quotes, but got: '%s'", buf->buffer);
        return -1;
    }
    else {
        LOG_LEXEM("character", buf->buffer);
    }
    BEGIN(INITIAL);
}

<STRING>[^\"\n%]*   { strbuf_append(buf, yytext); }

<STRING>\n          { ERROR("unclosed string"); return -1; }
<STRING><<EOF>>     { ERROR("unclosed string"); return -1; }

<STRING>\" {
    // Добавил проверку на режим дебага, чтобы не выделять память,
    // на экранирование строки, если это не нужно
    #ifdef DEBUG_LEXER
        char* escaped = escape(buf->buffer);
        LOG_LEXEM("string content", escaped);
        free(escaped);
    #endif

    BEGIN(INITIAL);
}

\"\[\n {
    strbuf_clear(buf);
    strlist_clear(verbatim_str);
    BEGIN(VERBATIM_ALIGNED_STRING);
}

<VERBATIM_ALIGNED_STRING>[ \t]*\]\"[ \t]*\n? {
    adjust_unaligned_verbatim_string(verbatim_str);
    for (int i = 0; i < strlist_count(verbatim_str); i++) {
        strbuf_append(buf, strlist_get(verbatim_str, i));
    }

    // Добавил проверку на режим дебага, чтобы не выделять память,
    // на экранирование строки, если это не нужно
    #ifdef DEBUG_LEXER
        char* escaped = escape(buf->buffer);
        LOG_LEXEM("verbatim string", escaped);
        free(escaped);
    #endif

    BEGIN(INITIAL);
}

<VERBATIM_ALIGNED_STRING>.*\n { strlist_push(verbatim_str, yytext); }

<VERBATIM_ALIGNED_STRING><<EOF>> { ERROR("unclosed verbatim string"); return -1; }

\" {
    strbuf_clear(buf);
    BEGIN(STRING);
}

\' {
    strbuf_clear(buf);
    BEGIN(CHARACTER);
}

{IDENTIFIER} {
    strbuf_clear(buf);
    strbuf_append(buf, yytext);
    LOG_LEXEM("identifier", buf->buffer);
}

{INT_10} {
    int line_start = yylineno;
    char* yycopy = strdup(yytext);

    char nc = input();
    if (nc != EOF && nc != '\0' && (isalpha(nc) || nc == '"' || nc == '\'' || nc == '_')) {
        strbuf_clear(buf);
        strbuf_append(buf, yycopy);
        do {
            strbuf_append_char(buf, nc);
            nc = input();
        } while (nc != EOF && nc != '\0' && !isdelim(nc));

        ERROR_F(line_start, "invalid decimal integer literal: \"%s\"", buf->buffer);
    }
    else {
        unput(nc);
        parse_integer(&int_number, yycopy, 10);
        LOG_LEXEM("decimal integer literal", yycopy);
    }

    free(yycopy);
}

{INT_16} {
    int line_start = yylineno;
    char* yycopy = strdup(yytext);

    char nc = input();
    if (nc != EOF && nc != '\0' && ((isalpha(nc) && !isxdigit(nc)) || nc == '"' || nc == '\'' || nc == '_')) {
        strbuf_clear(buf);
        strbuf_append(buf, yycopy);
        do {
            strbuf_append_char(buf, nc);
            nc = input();
        } while (nc != EOF && nc != '\0' && !isdelim(nc));

        ERROR_F(line_start, "invalid hexadecimal integer literal: \"%s\"", buf->buffer);
    }
    else {
        unput(nc);
        parse_integer(&int_number, yycopy, 16);
        LOG_LEXEM("hexadecimal integer literal", yycopy);
    }

    free(yycopy);
}

{INT_8} {
    int line_start = yylineno;
    char* yycopy = strdup(yytext);

    char nc = input();
    if (nc != EOF && nc != '\0' && (isalpha(nc) || nc == '"' || nc == '\'' || !isoctdigit(nc) || nc == '_')) {
        strbuf_clear(buf);
        strbuf_append(buf, yycopy);
        do {
            strbuf_append_char(buf, nc);
            nc = input();
        } while (nc != EOF && nc != '\0' && !isdelim(nc));

        ERROR_F(line_start, "invalid octal integer literal: \"%s\"", buf->buffer);
    }
    else {
        unput(nc);
        parse_integer(&int_number, yycopy, 8);
        LOG_LEXEM("octal integer literal", yycopy);
    }

    free(yycopy);
}

{INT_2} {
    int line_start = yylineno;
    char* yycopy = strdup(yytext);

    char nc = input();
    if (nc != EOF && nc != '\0' && (isalpha(nc) || nc == '"' || nc == '\'' || !isbindigit(nc) || nc == '_')) {
        strbuf_clear(buf);
        strbuf_append(buf, yycopy);
        do {
            strbuf_append_char(buf, nc);
            nc = input();
        } while (nc != EOF && nc != '\0' && !isdelim(nc));

        ERROR_F(line_start, "invalid binary integer literal: \"%s\"", buf->buffer);
    }
    else {
        unput(nc);
        parse_integer(&int_number, yycopy, 2);
        LOG_LEXEM("binary integer literal", yycopy);
    }

    free(yycopy);
}

{REAL_NUMBER} {
    int line_start = yylineno;
    char* yycopy = strdup(yytext);

    char nc = input();
    if (nc != EOF && nc != '\0' && (isalpha(nc) || nc == '"' || nc == '\'' || nc == '_')) {
        strbuf_clear(buf);
        strbuf_append(buf, yycopy);
        do {
            strbuf_append_char(buf, nc);
            nc = input();
        } while (nc != EOF && nc != '\0' && !isdelim(nc));

        ERROR_F(line_start, "invalid real number literal: \"%s\"", buf->buffer);
    }
    else {
        unput(nc);
        parse_real(&real_number, yytext);
        LOG_LEXEM("real number literal", yycopy);
    }

    free(yycopy);
}

{REAL_NUMBER_EXPONENT} {
    int line_start = yylineno;
    char* yycopy = strdup(yytext);

    char nc = input();
    if (nc != EOF && nc != '\0' && (isalpha(nc) || nc == '"' || nc == '\'')) {
        strbuf_clear(buf);
        strbuf_append(buf, yycopy);
        do {
            strbuf_append_char(buf, nc);
            nc = input();
        } while (nc != EOF && nc != '\0' && !isdelim(nc));

        ERROR_F(line_start, "invalid real exponent number literal: \"%s\"", buf->buffer);
    }
    else {
        unput(nc);
        parse_real(&real_number, yytext);
        LOG_LEXEM("real exponent number literal", yycopy);
    }

    free(yycopy);
}

{WHITESPACE} { }

. { LOG_LEXEM("unknown symbol", yytext); }


%%


int main(void) {
    yylex();
}
