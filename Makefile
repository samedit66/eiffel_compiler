CC = gcc

FLEX_FILE = src/eiffel.flex
LEX_YY_C_FILE = lex.yy.c
LEXER_EXE_NAME = lexer

LEXER_TEST_FILE = program.e

.PHONY: build
build: clean flex $(LEX_YY_C_FILE)
	$(CC) $(LEX_YY_C_FILE) -o $(LEXER_EXE_NAME)

.PHONY: flex
flex: $(FLEX_FILE)
	flex ./$(FLEX_FILE)

.PHONY: clean
clean:
	rm -rf $(wildcard *.exe) $(wildcard *.o) $(LEX_YY_C_FILE)

.PHONY: test
test:
	cat ./$(LEXER_TEST_FILE) | ./$(LEXER_EXE_NAME)
