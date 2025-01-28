import json
import sys

from backend.tree import make_ast
from backend.semantic.stage0 import process_stage0
from backend.execute import run_eiffel_parser
from backend.semantic.stage1 import process_stage1


eiffel_code = """
class ANY
feature
    default_create do end

    out: STRING do end
end

class STRING end

class A
inherit ANY rename default_create as dick redefine out end
feature common do end
feature out: STRING do end
end

class B
feature common do end
end

class C
inherit
    A rename out as A_out end
    B select common end
end

class D inherit C end
"""

def pretty_ftable(ftable):
    implicit = [f"{record.class_name}:{record.name}" for record in ftable.implicit]
    features = [f"{record.class_name}:{record.name}" for record in ftable.features]
    return f"[{" ".join(implicit + features)}]"


json_ast, stderr = run_eiffel_parser(eiffel_code, "build/eiffelp.exe")
if stderr:
    print(stderr, file=sys.stderr)
    sys.exit(1)

dict_ast = json.loads(json_ast)

ast = make_ast(dict_ast)

classes = process_stage0(ast)

ftable = process_stage1(classes)[5].features
print(pretty_ftable(ftable))