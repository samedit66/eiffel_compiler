SOURCES=src
EXECUTABLE=eiffelc

.PHONY: build
build:
	$(MAKE) -C $(SOURCES) build
	mv ./$(SOURCES)/$(EXECUTABLE) ./

.PHONY: clean
clean:
	rm -rf ./$(EXECUTABLE)
	$(MAKE) -C $(SOURCES) clean

.PHONY: test
test: $(EXECUTABLE)
	pytest -v
