CC=gcc
CFLAGS=-c -Wall
LDFLAGS=
SETTINGS=-DDEBUG_LEXER -DCOLORFUL
SOURCES=$(wildcard *.c)
OBJECTS=$(SOURCES:.c=.o)
EXECUTABLE=lexer
FLEX_FILE=eiffel.flex
FLEX_OUTPUT=lex.yy.c

.PHONY: build
build: clean flex $(SOURCES) $(EXECUTABLE)

.PHONY: flex
flex: $(FLEX_FILE)
	flex $<
	$(CC) $(CFLAGS) $(SETTINGS) $(FLEX_OUTPUT) -o $(FLEX_OUTPUT:.c=.o)

$(EXECUTABLE): $(OBJECTS) 
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@

.c.o:
	$(CC) $(CFLAGS) $(SETTINGS) $< -o $@

.PHONY: clean
clean:
	rm -rf $(OBJECTS) $(EXECUTABLE) $(FLEX_OUTPUT)

.PHONY: test
# TEST_FILE передается из внешнего Makefile
test:
	cat $(TEST_FILE) | ./$(EXECUTABLE)
