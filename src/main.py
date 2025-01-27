import json
import sys

from backend.tree import make_ast
from backend.semantic.stage0 import process_stage0
from backend.execute import run_eiffel_parser
from backend.semantic.stage1 import process_stage1
from backend.semantic.stage2.stage2 import process_stage2
from backend.semantic.stage2.types import TypedClass


eiffel_code = """
class ANY end

feature

    f
    local
        a: INTEGER
    do
        a := 
    end

end

class NONE
end

class T
    
end

class BOOLEAN
end
"""

json_ast, stderr = run_eiffel_parser(eiffel_code, "build/eiffelp.exe")
if stderr:
    print(stderr, file=sys.stderr)
    sys.exit(1)

dict_ast = json.loads(json_ast)

ast = make_ast(dict_ast)

classes = process_stage0(ast)
flatten_classes = process_stage1(classes)

classes = process_stage2(flatten_classes)
print(classes)
