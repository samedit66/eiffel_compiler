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

# If the first argument is "view"...
ifeq (view,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "view"
  RUN_ARGS = $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

.PHONY: view
view: $(EXECUTABLE)
	@python ./test/visualize.py $(RUN_ARGS)
