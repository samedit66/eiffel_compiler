CC = gcc
CFLAGS = -Wall
SETTINGS = -DDEBUG_LEXER -DCOLORFUL

FLEX_FILE = src/eiffel.flex
LEX_YY_C_FILE = lex.yy.c
LEXER_EXE_NAME = lexer
LEXER_TEST_FILE = program.e

.PHONY: build
build: clean flex
	$(CC) $(CFLAGS) $(SETTINGS) ./src/$(LEX_YY_C_FILE) -o $(LEXER_EXE_NAME)

.PHONY: flex
flex: $(FLEX_FILE)
	flex ./$(FLEX_FILE)
	mv ./$(LEX_YY_C_FILE) ./src/

.PHONY: clean
clean:
	rm -rf $(wildcard *.exe) $(wildcard *.o) ./src/$(LEX_YY_C_FILE)

.PHONY: test
test: build
	cat ./$(LEXER_TEST_FILE) | ./$(LEXER_EXE_NAME)
