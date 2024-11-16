import subprocess


def run_eiffel_parser(
        eiffel_text: str,
        parser_name: str = "eiffelc",
        ) -> tuple[str, str]:
    """
    Возвращает результат работы парсера Eiffel по заданному файлу

    :param eiffel_text текст программы на Eiffel
    :param parser_name имя парсера
    """
    output = subprocess.run(
        [parser_name],
        input=eiffel_text.encode(),
        capture_output=True,
        )
    return (output.stdout.decode(), output.stdout.decode())


def test_empty_class():
    input_data = """
    class
        SIMPLE
    end
    """
    
    _, stderr = run_eiffel_parser(input_data)

    assert "syntax error" not in stderr


def test_simple_inheritance_with_rename():
    input_data = """
    class SQUARE
        inherit
            RECTANGLE
            rename
                width as size
            end
    end
    """

    _, stderr = run_eiffel_parser(input_data)

    assert "syntax error" not in stderr


def test_class_with_feature():
    input_data = """
    class
      APPLICATION

    create
      make

    feature -- Initialization

      make
          -- Run application.
        do
          io.put_string ("Hello, world")
          io.put_new_line
        end

    end -- class APPLICATION
    """

    _, stderr = run_eiffel_parser(input_data)

    assert "syntax error" not in stderr
