.PHONY: build
build:
	$(MAKE) -C src

.PHONY: clean
clean:
	$(MAKE) -C src clean

.PHONY: test
export TEST_FILE=../program.e
test:
	$(MAKE) -C src test
