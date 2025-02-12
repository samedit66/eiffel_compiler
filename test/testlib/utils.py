from pathlib import Path
import subprocess
import re


def replace_rn_with_n(string: str) -> str:
    return "\n".join(string.splitlines())


def run_eiffel_parser(
        program: str,
        parser_path: str | Path,
        ) -> tuple[str, str]:
    """Возвращает результат работы парсера Eiffel по заданному файлу

    :param program: текст программы на Eiffel
    :param parser_path: путь к парсеру, включая имя файла парсера

    :return: кортеж из двух строк: stdout и stderr
    """
    try:
        output = subprocess.run(
            [parser_path],
            input=program.encode(),
            capture_output=True,
            )
    except FileNotFoundError:
        raise RuntimeError(f'Couldn\'t find eiffel parser by path "{parser_path}"')
    stdout, stderr = output.stdout.decode(), output.stderr.decode()
    return replace_rn_with_n(stdout), replace_rn_with_n(stderr)


def make_error_message(stderr):
    """Считывает все сообщения об ошибках из stderr

    :param stderr: сообщения из stderr потока

    :return: сообщение об ошибках
    """
    errors = re.findall(r'error: .*\n?', stderr)
    return '\n'.join(errors)
