%{
    #include <ctype.h>
    #include <stdio.h>
    #include <stdint.h>
    #include <stdbool.h>
    #include <string.h>
    #include <ctype.h>

    #include "./include/lex_utils.h"
    #include "./include/strbuf.h"
    #include "./include/strlist.h"
    #include "eiffel.tab.h"

    #define yyterminate() return EOI

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
        fprintf(stderr, "Line %d: " RED_TEXT ": ", lineno, "error");\
        fprintf(stderr, msg, __VA_ARGS__);\
        fprintf(stderr, "\n");\
    }

    #define ERROR_AT_LINENO(lineno, msg)\
        fprintf(stderr, "Line %d: " RED_TEXT ": %s", lineno, "error", msg)

    #define ERROR(msg) ERROR_AT_LINENO(yylineno, msg)
%}

%option noyywrap
%option yylineno
%option never-interactive
%option array


IDENTIFIER [_a-zA-Z][_a-zA-Z0-9]*

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
    StringBuffer *buf = StringBuffer_empty();
    StringList *verbatim_str = StringList_new();
%}

":="					{ LOG_LEXEM("operator", ":="); return ASSIGN_TO; }
"="						{ LOG_LEXEM("operator", "EQUALS"); return '='; }
"/="					{ LOG_LEXEM("operator", "NOT_EQUALS"); return NEQ; }
"<" 					{ LOG_LEXEM("operator", "LESS"); return '<'; }
"<=" 					{ LOG_LEXEM("operator", "LESS_OR_EQUAL"); return LE; }
">" 					{ LOG_LEXEM("operator", "GREATER"); return '>'; }
">=" 					{ LOG_LEXEM("operator", "GREATER_OR_EQUAL"); return GE; }
"and" 					{ LOG_LEXEM("operator", "AND"); return AND; }
"xor" 					{ LOG_LEXEM("operator", "XOR"); return XOR; }
"or" 					{ LOG_LEXEM("operator", "OR"); return OR; } 
"not" 					{ LOG_LEXEM("operator", "NOT"); return NOT;}
and{WHITESPACE}then 	{ LOG_LEXEM("operator", "AND_THEN"); return AND_THEN; }
or{WHITESPACE}else 	    { LOG_LEXEM("operator", "OR_ELSE"); return OR_ELSE; }
"implies" 				{ LOG_LEXEM("operator", "IMPLIES"); return IMPLIES; }
"//"					{ LOG_LEXEM("operator", "DIV"); return INT_DIV; }
"\\\\"					{ LOG_LEXEM("operator", "MOD"); return MOD; }
"+" 					{ LOG_LEXEM("operator", "+"); return '+'; }
"-" 					{ LOG_LEXEM("operator", "-"); return '-'; }
"*" 					{ LOG_LEXEM("operator", "*"); return '*'; }
"/"						{ LOG_LEXEM("operator", "/"); return '/'; }
"^" 					{ LOG_LEXEM("operator", "^"); return '^'; }
";" 					{ LOG_LEXEM("operator", ";"); return ';'; }

"->"                    { LOG_LEXEM("symbol", "->"); return RARROW; }
"<<"                    { LOG_LEXEM("symbol", "<<"); }
">>"                    { LOG_LEXEM("symbol", ">>"); }
"(" 					{ LOG_LEXEM("symbol", "("); return '('; }
")" 					{ LOG_LEXEM("symbol", ")"); return ')'; }
"{" 					{ LOG_LEXEM("symbol", "{"); return '{'; }
"}" 					{ LOG_LEXEM("symbol", "}"); return '}'; }
"[" 					{ LOG_LEXEM("symbol", "["); return '['; }
"]" 					{ LOG_LEXEM("symbol", "]"); return ']'; }
":" 					{ LOG_LEXEM("symbol", ":"); return ':'; }
".."                    { LOG_LEXEM("symbol", ".."); return TWO_DOTS; }
"." 					{ LOG_LEXEM("symbol", "."); return '.'; }
"," 					{ LOG_LEXEM("symbol", ","); return ','; }

"all" 					{ LOG_LEXEM("keyword", "ALL"); }
"across"                { LOG_LEXEM("keyword", "ACROSS"); }
"agent"                 { LOG_LEXEM("keyword", "AGENT"); }
"alias"                 { LOG_LEXEM("keyword", "ALIAS"); }
"as"                    { LOG_LEXEM("keyword", "AS"); return AS; }
"assign"                { LOG_LEXEM("keyword", "ASSIGN"); }
"attribute"             { LOG_LEXEM("keyword", "ATTRIBUTE"); }
"class" 				{ LOG_LEXEM("keyword", "CLASS"); return CLASS; }
"check"                 { LOG_LEXEM("keyword", "CHECK"); }
"convert"               { LOG_LEXEM("keyword", "CONVERT"); }
"create" 				{ LOG_LEXEM("keyword", "CREATE"); return CREATE; }
"Current" 				{ LOG_LEXEM("keyword", "CURRENT"); return CURRENT; }
"do" 					{ LOG_LEXEM("keyword", "DO"); return DO; }
"debug"                 { LOG_LEXEM("keyword", "DEBUG"); }
"deferred"              { LOG_LEXEM("keyword", "DEFERRED"); }
"else" 					{ LOG_LEXEM("keyword", "ELSE"); return ELSE; }
"elseif" 				{ LOG_LEXEM("keyword", "ELSEIF"); return ELSEIF; }
"end" 					{ LOG_LEXEM("keyword", "END"); return END; }
"ensure"                { LOG_LEXEM("keyword", "ENSURE"); return ENSURE; }
"expanded"              { LOG_LEXEM("keyword", "EXPANDED"); }
"export"                { LOG_LEXEM("keyword", "EXPORT"); }
"external"              { LOG_LEXEM("keyword", "EXTERNAL"); }
"feature" 				{ LOG_LEXEM("keyword", "FEATURE"); return FEATURE; }
"from" 					{ LOG_LEXEM("keyword", "FROM"); return FROM; }
"False"                 { LOG_LEXEM("keyword", "FALSE"); return FALSE_KW; }
"frozen"                { LOG_LEXEM("keyword", "FROZEN"); }
"if" 					{ LOG_LEXEM("keyword", "IF"); return IF; }
"inherit" 				{ LOG_LEXEM("keyword", "INHERIT"); }
"inspect"               { LOG_LEXEM("keyword", "INSPECT"); return INSPECT; }
"invariant"             { LOG_LEXEM("keyword", "INVARIANT"); }
"local" 				{ LOG_LEXEM("keyword", "LOCAL"); return LOCAL; }
"loop" 					{ LOG_LEXEM("keyword", "LOOP"); return LOOP;}
"like"                  { LOG_LEXEM("keyword", "LIKE"); return LIKE; }
"note" 					{ LOG_LEXEM("keyword", "NOTE"); }
"obsolete"              { LOG_LEXEM("keyword", "OBSOLETE"); }
"old"                   { LOG_LEXEM("keyword", "OLD"); }
"once"                  { LOG_LEXEM("keyword", "ONCE"); }
"only"                  { LOG_LEXEM("keyword", "ONLY"); }
"Precursor" 			{ LOG_LEXEM("keyword", "PRECURSOR"); return PRECURSOR; }
"redefine" 				{ LOG_LEXEM("keyword", "REDEFINE"); return REDEFINE; }
"rename" 				{ LOG_LEXEM("keyword", "RENAME"); return RENAME; }
"Result" 				{ LOG_LEXEM("keyword", "RESULT"); return RESULT; }
"require"               { LOG_LEXEM("keyword", "REQUIRE"); return REQUIRE; }
"rescue"                { LOG_LEXEM("keyword", "RESCUE"); }
"retry"                 { LOG_LEXEM("keyword", "RETRY"); }
"separate"              { LOG_LEXEM("keyword", "SEPARATE"); }
"select" 				{ LOG_LEXEM("keyword", "SELECT"); return SELECT; }
"then" 					{ LOG_LEXEM("keyword", "THEN"); return THEN; }
"True"                  { LOG_LEXEM("keyword", "TRUE");  return TRUE_KW; }
"undefine" 				{ LOG_LEXEM("keyword", "UNDEFINE"); return UNDEFINE; }
"until" 				{ LOG_LEXEM("keyword", "UNTIL"); return UNTIL; }
"variant"               { LOG_LEXEM("keyword", "VARIANT"); }
"Void"                  { LOG_LEXEM("keyword", "VOID");  return VOID; }
"when"                  { LOG_LEXEM("keyword", "WHEN"); return WHEN; }

"ARRAY" 				{ LOG_LEXEM("keyword", "ARRAY"); return ARRAY; }
"INTEGER" 				{ LOG_LEXEM("keyword", "INTEGER"); return INTEGER; }
"REAL" 					{ LOG_LEXEM("keyword", "REAL"); return REAL; }
"CHARACTER" 			{ LOG_LEXEM("keyword", "CHARACTER"); return CHARACTER; }
"STRING" 				{ LOG_LEXEM("keyword", "STRING"); return STRING_KW; }
"TUPLE"                 { LOG_LEXEM("keyword", "TUPLE"); return TUPLE; }
"BOOLEAN" 				{ LOG_LEXEM("keyword", "BOOLEAN"); return BOOLEAN; }


--.*\n? { LOG_LEXEM("single line comment", yytext); }

<CHARACTER,STRING>%\/[0-9]{1,3}\/ {
    StringBuffer_append_char(buf, convert_decimal_encoded_char(yytext));
}
<CHARACTER,STRING>%%      { StringBuffer_append_char(buf, '%'); }
<CHARACTER,STRING>%[nN]   { StringBuffer_append_char(buf, '\n'); }
<CHARACTER,STRING>%[tT]   { StringBuffer_append_char(buf, '\t'); }
<CHARACTER,STRING>%[aA]   { StringBuffer_append_char(buf, '@'); }
<CHARACTER,STRING>%[bB]   { StringBuffer_append_char(buf, '\b'); }
<CHARACTER,STRING>%[cC]   { StringBuffer_append_char(buf, '^'); }
<CHARACTER,STRING>%[dD]   { StringBuffer_append_char(buf, '$'); }
<CHARACTER,STRING>%[fF]   { StringBuffer_append_char(buf, '\f'); }
<CHARACTER,STRING>%[hH]   { StringBuffer_append_char(buf, '\\'); }
<CHARACTER,STRING>%[lL]   { StringBuffer_append_char(buf, '~'); }
<CHARACTER,STRING>%[qQ]   { StringBuffer_append_char(buf, '`'); }
<CHARACTER,STRING>%[rR]   { StringBuffer_append_char(buf, '\r'); }
<CHARACTER,STRING>%[sS]   { StringBuffer_append_char(buf, '#'); }
<CHARACTER,STRING>%[uU]   { StringBuffer_append_char(buf, '\0'); }
<CHARACTER,STRING>%[vV]   { StringBuffer_append_char(buf, '\v'); }
<CHARACTER,STRING>%\(     { StringBuffer_append_char(buf, '['); }
<CHARACTER,STRING>%\)     { StringBuffer_append_char(buf, ']'); }
<CHARACTER,STRING>%\<     { StringBuffer_append_char(buf, '{'); }
<CHARACTER,STRING>%\>     { StringBuffer_append_char(buf, '}'); }
<CHARACTER,STRING>%\"     { StringBuffer_append_char(buf, '\"'); }
<CHARACTER,STRING>%\'     { StringBuffer_append_char(buf, '\''); }
<CHARACTER,STRING>%(.|\n) { ERROR("invalid escape sequence"); }

<CHARACTER>[^\'\n]* {
    StringBuffer_append(buf, yytext);
    
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
    
    yylval.int_num = buf->buffer[0];
    return CHAR_CONST;
}

<STRING>[^\"\n%]*   { StringBuffer_append(buf, yytext); }

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
    return STRING_CONST;
}

\"\[\n {
    StringBuffer_clear(buf);
    StringList_clear(verbatim_str);
    BEGIN(VERBATIM_ALIGNED_STRING);
}

<VERBATIM_ALIGNED_STRING>[ \t]*\]\"[ \t]*\n? {
    adjust_unaligned_verbatim_string(verbatim_str);
    // TODO: Когда-нибудь переписать через StringList_join
    for (int i = 0; i < StringList_size(verbatim_str); i++) {
        StringBuffer_append(buf, StringList_get(verbatim_str, i));
    }

    // Добавил проверку на режим дебага, чтобы не выделять память,
    // на экранирование строки, если это не нужно
    #ifdef DEBUG_LEXER
        char* escaped = escape(buf->buffer);
        LOG_LEXEM("verbatim string", escaped);
        free(escaped);
    #endif

    BEGIN(INITIAL);
    return STRING_CONST;
}

<VERBATIM_ALIGNED_STRING>.*\n { StringList_push(verbatim_str, yytext); }

<VERBATIM_ALIGNED_STRING><<EOF>> { ERROR("unclosed verbatim string"); return -1; }

\" {
    StringBuffer_clear(buf);
    BEGIN(STRING);
}

\' {
    StringBuffer_clear(buf);
    BEGIN(CHARACTER);
}

{IDENTIFIER} {
    StringBuffer_clear(buf);
    StringBuffer_append(buf, yytext);
    LOG_LEXEM("identifier", buf->buffer);
    yylval.name = buf->buffer;
    return IDENT_LIT;
}

{INT_10} {
    int line_start = yylineno;

    char nc = input();
    if (nc != EOF && nc != '\0' && (isalpha(nc) || nc == '"' || nc == '\'' || nc == '_') && !is_delim(nc)) {
        StringBuffer_clear(buf);
        StringBuffer_append(buf, yytext);
        do {
            StringBuffer_append_char(buf, nc);
            nc = input();
        } while (nc != EOF && nc != '\0' && !is_delim(nc));

        unput(nc);
        ERROR_F(line_start, "invalid decimal integer literal: \"%s\"", buf->buffer);
    }
    else {
        unput(nc);
        parse_int(yytext, &int_number, 10);
        LOG_LEXEM("decimal integer literal", yytext);
        
        yylval.int_num = int_number;
        return INT_CONST;
    }
}

{INT_16} {
    int line_start = yylineno;

    char nc = input();
    if (nc != EOF && nc != '\0' && ((isalpha(nc) && !isxdigit(nc)) || nc == '"' || nc == '\'' || nc == '_') && !is_delim(nc)) {
        StringBuffer_clear(buf);
        StringBuffer_append(buf, yytext);
        do {
            StringBuffer_append_char(buf, nc);
            nc = input();
        } while (nc != EOF && nc != '\0' && !is_delim(nc));

        ERROR_F(line_start, "invalid hexadecimal integer literal: \"%s\"", buf->buffer);
    }
    else {
        unput(nc);
        parse_int(yytext, &int_number, 16);
        LOG_LEXEM("hexadecimal integer literal", yytext);
        
        yylval.int_num = int_number;
        return INT_CONST;
    }
}

{INT_8} {
    int line_start = yylineno;

    char nc = input();
    if (nc != EOF && nc != '\0' && (isalpha(nc) || nc == '"' || nc == '\'' || !is_oct_digit(nc) || nc == '_') && !is_delim(nc)) {
        StringBuffer_clear(buf);
        StringBuffer_append(buf, yytext);
        do {
            StringBuffer_append_char(buf, nc);
            nc = input();
        } while (nc != EOF && nc != '\0' && !is_delim(nc));

        ERROR_F(line_start, "invalid octal integer literal: \"%s\"", buf->buffer);
    }
    else {
        unput(nc);
        parse_int(yytext, &int_number, 8);
        LOG_LEXEM("octal integer literal", yytext);

        yylval.int_num = int_number;
        return INT_CONST;
    }
}

{INT_2} {
    int line_start = yylineno;

    char nc = input();
    if (nc != EOF && nc != '\0' && (isalpha(nc) || nc == '"' || nc == '\'' || !is_bin_digit(nc) || nc == '_') && !is_delim(nc)) {
        StringBuffer_clear(buf);
        StringBuffer_append(buf, yytext);
        do {
            StringBuffer_append_char(buf, nc);
            nc = input();
        } while (nc != EOF && nc != '\0' && !is_delim(nc));

        ERROR_F(line_start, "invalid binary integer literal: \"%s\"", buf->buffer);
    }
    else {
        unput(nc);
        parse_int(yytext, &int_number, 2);
        LOG_LEXEM("binary integer literal", yytext);

        yylval.int_num = int_number;
        return INT_CONST;
    }
}

{REAL_NUMBER} {
    int line_start = yylineno;

    char nc = input();
    if (yytext[strlen(yytext) - 1] == '.' && nc == '.') {
        unput(nc);
        REJECT;
    }

    if (nc != EOF && nc != '\0' && (isalpha(nc) || nc == '"' || nc == '\'' || nc == '_') && !is_delim(nc)) {
        StringBuffer_clear(buf);
        StringBuffer_append(buf, yytext);
        do {
            StringBuffer_append_char(buf, nc);
            nc = input();
        } while (nc != EOF && nc != '\0' && !is_delim(nc));

        ERROR_F(line_start, "invalid real number literal: \"%s\"", buf->buffer);
    }
    else {
        unput(nc);
        parse_real(yytext, &real_number);
        LOG_LEXEM("real number literal", yytext);

        yylval.real_num = real_number;
        return REAL_CONST;
    }
}

{REAL_NUMBER_EXPONENT} {
    int line_start = yylineno;

    char nc = input();
    if (nc != EOF && nc != '\0' && (isalpha(nc) || nc == '"' || nc == '\'') && !is_delim(nc)) {
        StringBuffer_clear(buf);
        StringBuffer_append(buf, yytext);
        do {
            StringBuffer_append_char(buf, nc);
            nc = input();
        } while (nc != EOF && nc != '\0' && !is_delim(nc));

        ERROR_F(line_start, "invalid real exponent number literal: \"%s\"", buf->buffer);
    }
    else {
        unput(nc);
        parse_real(yytext, &real_number);
        LOG_LEXEM("real exponent number literal", yytext);

        yylval.real_num = real_number;
        return REAL_CONST;
    }
}

{WHITESPACE} { }

. {
    if (yytext[0] != '\0') {
        LOG_LEXEM("unknown symbol", yytext);
    }
}


%%
