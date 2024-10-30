CC=gcc
CFLAGS=-c -Wall
LDFLAGS=

SETTINGS=-DCOLORFUL #-DDEBUG_LEXER 

SOURCES=$(wildcard *.c)
OBJECTS=$(SOURCES:.c=.o)
EXECUTABLE=eiffelc

FLEX_FILE=eiffel.flex
FLEX_OUTPUT=lex.yy.c

BISON_FILE=eiffel.y
BISON_OUTPUT_C=eiffel.tab.c
BISON_OUTPUT_H=eiffel.tab.h

.PHONY: build
build: clean bison flex $(SOURCES) $(EXECUTABLE)

.PHONY: bison
bison: $(BISON_FILE)
	bison -Wcounterexamples -d $<
	$(CC) $(CFLAGS) $(SETTINGS) $(BISON_OUTPUT_C) -o $(BISON_OUTPUT_C:.c=.o)

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
	rm -rf $(OBJECTS) $(EXECUTABLE) $(FLEX_OUTPUT) $(BISON_OUTPUT_H) $(BISON_OUTPUT_C)
