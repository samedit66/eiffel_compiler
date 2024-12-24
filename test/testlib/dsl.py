from pathlib import Path
import functools
import json

from testlib.utils import (
    run_eiffel_parser,
    make_error_message,
    )
from testlib.config import (
    PARSER_BUILD_PATH,
    TEST_EXAMPLES_DIR,
)


def expect(tree, *, full_match=False):
    
    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            expected_json = json.dumps(tree, separators=(',', ':'))

            generated_json, stderr = func(*args, **kwargs)
            
            if full_match:
                assert expected_json == generated_json, make_error_message(stderr) or ""
            else:
                assert expected_json in generated_json, make_error_message(stderr) or ""

        return wrapper
    
    return decorator


def run_eiffel(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        program_text = func(*args, **kwargs)
        return run_eiffel_parser(program_text, PARSER_BUILD_PATH)

    return wrapper


def use(example_file, examples_dir=TEST_EXAMPLES_DIR):

    def decorator(func):
        file_contents = (examples_dir/example_file).read_text()

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return file_contents

        return wrapper
    
    return decorator
