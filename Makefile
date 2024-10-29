SOURCES=src
EXECUTABLE=eiffelc
TEST_FILE=program.e

.PHONY: build
build:
	$(MAKE) -C $(SOURCES) build
	mv $(SOURCES)/$(EXECUTABLE) ./

.PHONY: clean
clean:
	rm -rf $(EXECUTABLE)
	$(MAKE) -C $(SOURCES) clean

.PHONY: test
test: $(EXECUTABLE)
	cat $(TEST_FILE) | ./$(EXECUTABLE)
