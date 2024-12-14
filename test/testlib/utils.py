import subprocess
import re


def replace_rn_with_n(string: str) -> str:
    return "\n".join(string.splitlines())


def run_eiffel_parser(
        program: str,
        parser_name: str = "eiffelp",
        ) -> tuple[str, str]:
    """Возвращает результат работы парсера Eiffel по заданному файлу

    :param program: текст программы на Eiffel
    :param parser_name: имя парсера

    :return: кортеж из двух строк: stdout и stderr
    """
    try:
        output = subprocess.run(
            [parser_name],
            input=program.encode(),
            capture_output=True,
            )
    except FileNotFoundError:
        raise RuntimeError(f'Couldn\'t find eiffel parser by name "{parser_name}"')
    stdout, stderr = output.stdout.decode(), output.stderr.decode()
    return replace_rn_with_n(stdout), replace_rn_with_n(stderr)


def make_error_message(stderr: str):
    """Считывает все сообщения об ошибках из stderr

    :param stderr: сообщения из stderr потока

    :return: сообщение об ошибках
    """
    errors = re.findall(r'error: .*\n?', stderr)
    return '\n'.join(errors)
