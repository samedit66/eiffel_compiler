import subprocess


def run_eiffel_parser(
        eiffel_text: str,
        parser_name: str = "eiffelc",
        ) -> tuple[str, str]:
    """
    Возвращает результат работы парсера Eiffel по заданному файлу

    :param eiffel_text: текст программы на Eiffel
    :param parser_name: имя парсера

    :return: кортеж из двух строк: stdout и stderr
    """
    try:
        output = subprocess.run(
            [parser_name],
            input=eiffel_text.encode(),
            capture_output=True,
            )
    except FileNotFoundError:
        raise RuntimeError(f'Couldn\'t find eiffel parser by name "{parser_name}"')
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


def test_class_with_different_types_of_features():
    input_data = """
    class
        FRACTION

    create
      make

    feature
        numerator, denominator: INTEGER

        sum (other: like Current): FRACTION
        do
            -- Nothing goes here
        end

        difference (other: FRACTION): FRACTION
        do
            -- Nothing goes here
        end

        product (other: FRACTION): FRACTION
        do
            -- Nothing goes here
        end

        quotient (other: FRACTION ): FRACTION
        do
            -- Nothing goes here
        end

        inverse: FRACTION do
            Result.make
        end

    feature {NONE}

    make (n, d: INTEGER) do
        numerator := n
        denominator := d
    end

    reduce do
        -- Nothing goes here
    end

    end -- class FRACTION
    """

    _, stderr = run_eiffel_parser(input_data)

    assert "syntax error" not in stderr


def test_different_feature_call():
    input_data = """
    class
        TEST_DIFFERENT_FEATURE_CALL
    
    feature

        test do
            test Result.make
            Precursor[10].call(1, 2, 3)
            Current.numerator
            (1 + 2).out
            a.b()
            array[1][2][3].call()
            f(1, 2, 3)
        end
    end
    """

    _, stderr = run_eiffel_parser(input_data)

    assert "syntax error" not in stderr


def test_inspect_stmt():
    input_data = """
    class
        TEST_INSPECT_STMT

    feature

        test do
            inspect a
                when 1, 2, 3 then print(1)
                when 5, 6..10 then print(2)
                when 11, 54..98, 99 then print(3)
                else print(4)
            end
        end
    end
    """

    _, stderr = run_eiffel_parser(input_data)

    assert "syntax error" not in stderr
