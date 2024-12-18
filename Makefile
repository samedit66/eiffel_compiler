SOURCES=src/parser
EXECUTABLE=eiffelp
BUILD_DIR=build

.PHONY: build
build:
	$(MAKE) -C $(SOURCES) ./$(BUILD_DIR)
	mkdir ./$(BUILD_DIR)
	mv ./$(SOURCES)/$(EXECUTABLE) ./$(BUILD_DIR)

.PHONY: debug
debug:
	$(MAKE) -C $(SOURCES) debug
	mkdir ./$(BUILD_DIR)
	mv ./$(SOURCES)/$(EXECUTABLE) ./$(BUILD_DIR)

.PHONY: clean
clean:
	rm -rf ./$(EXECUTABLE) ./$(BUILD_DIR)
	$(MAKE) -C $(SOURCES) clean

.PHONY: test
test: $(BUILD_DIR)/$(EXECUTABLE)
	@pytest -v

# If the first argument is "view"...
ifeq (view,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "view"
  VIEW_ARGS = $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(VIEW_ARGS):;@:)
endif

.PHONY: view
view: $(BUILD_DIR)/$(EXECUTABLE)
	@python ./test/visualize.py $(VIEW_ARGS)
