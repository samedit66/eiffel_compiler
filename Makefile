SOURCES=src
EXECUTABLE=eiffelp

.PHONY: build
build:
	$(MAKE) -C $(SOURCES) build
	mv ./$(SOURCES)/$(EXECUTABLE) ./

.PHONY: debug
debug:
	$(MAKE) -C $(SOURCES) debug
	mv ./$(SOURCES)/$(EXECUTABLE) ./

.PHONY: clean
clean:
	rm -rf ./$(EXECUTABLE)
	$(MAKE) -C $(SOURCES) clean

.PHONY: test
test: $(EXECUTABLE)
	pytest -v
