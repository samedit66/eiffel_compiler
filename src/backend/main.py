from pathlib import Path
import json
from pprint import pprint as pp

from execute import run_eiffel_parser
from tree.class_decl import ClassDecl


eiffel_code = """
class A
feature
    pi: REAL then 3.14 end
end
"""

program_dict = json.loads(
    run_eiffel_parser(eiffel_code, "build\\eiffelp.exe")[0]
)

print(ClassDecl.from_dict(program_dict["classes"][0]))