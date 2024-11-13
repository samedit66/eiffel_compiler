import subprocess


def run_eiffel_parser(file_name: str, parser_name: str = "eiffelc"):
    return subprocess.run([parser_name, file_name], capture_output=True)
