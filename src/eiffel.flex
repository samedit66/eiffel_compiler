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

REAL_NUMBER                {DECIMAL_NUMBER}?\.{DECIMAL_NUMBER}|{DECIMAL_NUMBER}\.{DECIMAL_NUMBER}?
REAL_NUMBER_EXPONENT       ({REAL_NUMBER}|{DECIMAL_NUMBER})[eE][\-+]?{DECIMAL_NUMBER}


%x SINGLE_LINE_COMMENT
%x CHARACTER
%x STRING
%x VERBATIM_ALIGNED_STRING


%%


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


<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%\/[0-9]{1,3}\/% { printf("Line %d: character decimal encoded\n", yylineno); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%%     { printf("Line %d: percent character\n", yylineno); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%[nN]  { printf("Line %d: newline character\n", yylineno); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%[tT]  { printf("Line %d: horizontal tab character\n", yylineno); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%[aA]  { printf("Line %d: at sign character\n", yylineno); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%[bB]  { printf("Line %d: backspace character\n", yylineno); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%[cC]  { printf("Line %d: circumflex character\n", yylineno); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%[dD]  { printf("Line %d: dollar character\n", yylineno); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%[fF]  { printf("Line %d: form feed character\n", yylineno); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%[hH]  { printf("Line %d: backslash character\n", yylineno); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%[lL]  { printf("Line %d: tilde character\n", yylineno); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%[qQ]  { printf("Line %d: backquote character\n", yylineno); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%[rR]  { printf("Line %d: carriage return character\n", yylineno); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%[sS]  { printf("Line %d: sharp character\n", yylineno); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%[uU]  { printf("Line %d: null character\n", yylineno); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%[vV]  { printf("Line %d: vertical bar character\n", yylineno); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%\(    { printf("Line %d: opening bracket character\n", yylineno); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%\)    { printf("Line %d: closing bracket character\n", yylineno); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%\<    { printf("Line %d: opening brace character\n", yylineno); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%\>    { printf("Line %d: closing brace character\n", yylineno); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%\"    { printf("Line %d: double quote character\n", yylineno); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%\'    { printf("Line %d: single quote character\n", yylineno); }
<CHARACTER,STRING,VERBATIM_ALIGNED_STRING>%.     { printf("Line %d: ERROR: invalid escape sequence\n", yylineno); return -1; }

<CHARACTER>[^\'\n]* { printf("Line %d: character content: %s\n", yylineno, yytext); }

<CHARACTER>\n       { printf("Line %d: ERROR: unclosed character\n", yylineno); return -1; }

<CHARACTER><<EOF>>  { printf("Line %d: ERROR: unclosed character\n", yylineno); return -1; }

<CHARACTER>\'       { printf("Line %d: character end\n", yylineno); BEGIN(INITIAL); }

<STRING>[^\"\n%]*   { printf("Line %d: part of string\n", yylineno); }

<STRING>\n          { printf("Line %d: ERROR: unclosed string\n", yylineno); return -1; }

<STRING><<EOF>>     { printf("Line %d: ERROR: unclosed string\n", yylineno); return -1; }

<STRING>\"          { printf("Line %d: string end\n", yylineno); BEGIN(INITIAL); }

\"\[\n?                                { printf("Line %d: verbatim aligned string start\n", yylineno); BEGIN(VERBATIM_ALIGNED_STRING); }

<VERBATIM_ALIGNED_STRING>\]\"          { printf("Line %d: verbatim aligned string end\n", yylineno); BEGIN(INITIAL); }

<VERBATIM_ALIGNED_STRING>([^\]%]*\n?)* { printf("Line %d: verbatim aligned string part\n", yylineno); }

<VERBATIM_ALIGNED_STRING>\]            { printf("Line %d: verbatim aligned string part bracket\n", yylineno); }

<VERBATIM_ALIGNED_STRING><<EOF>>       { printf("Line %d: ERROR: verbatium aligned string unclosed", yylineno); return -1; }

\"                                     { printf("Line %d: string start\n", yylineno); BEGIN(STRING); }

\'                                     { printf("Line %d: character start\n", yylineno); BEGIN(CHARACTER); }


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
