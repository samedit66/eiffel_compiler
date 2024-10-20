CC = gcc
CFLAGS = -Wall -I $(SOURCE_DIR)
SETTINGS = -DDEBUG_LEXER -DCOLORFUL

BUILD_DIR = build
SOURCE_DIR = src
FLEX_FILE = src/eiffel.flex
LEX_YY_C_FILE = lex.yy.c
LEXER_EXE_NAME = lexer
LEXER_TEST_FILE = program.e

.PHONY: build
build: clean prepare flex
	$(CC) $(CFLAGS) $(SETTINGS) ./$(BUILD_DIR)/$(LEX_YY_C_FILE) -o ./$(BUILD_DIR)/$(LEXER_EXE_NAME)

.PHONY: prepare
prepare:
	mkdir -p $(BUILD_DIR)

.PHONY: flex
flex: $(FLEX_FILE)
	flex ./$(FLEX_FILE)
	mv ./$(LEX_YY_C_FILE) ./$(BUILD_DIR)/

.PHONY: clean
clean:
	rm -rf $(BUILD_DIR)

.PHONY: test
test: build
	cat ./$(LEXER_TEST_FILE) | ./$(BUILD_DIR)/$(LEXER_EXE_NAME)
