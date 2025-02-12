import json
import sys

from serpent.tree import make_ast
from serpent.tree.abstract_node import Location
#from backend.semantic_сhecker.stage0 import process_stage0
from serpent.parser_adapter import parse
#from backend.semantic_сhecker.stage1 import process_stage1
from serpent.errors import *


eiffel_code = """class A
feature
    f
    do
        {CLASS} Precursor (1, 2, 3)
    end
end
"""

def pretty_ftable(ftable):
    implicit = [f"{record.class_name}:{record.name}" for record in ftable.implicit]
    features = [f"{record.class_name}:{record.name}" for record in ftable.features]
    return f"[{" ".join(implicit)}]", f"[{" ".join(features)}]"


json_ast, stderr = parse(eiffel_code, "build/eiffelp.exe")
if stderr:
    print(stderr, file=sys.stderr)
    sys.exit(1)

dict_ast = json.loads(json_ast)

ast = make_ast(dict_ast)

error_collector = ErrorCollector()

error_collector.add_error(CompilerError("what the fuck just happened?"))
error_collector.show()
