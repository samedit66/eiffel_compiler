import json
import sys

from backend.tree import make_ast
from backend.semantic.stage0.stage0 import process_stage0
from backend.execute import run_eiffel_parser
from backend.semantic.stage1.inheritance import analyze_inheritance


eiffel_code = """
class ANY end

class A feature g: INTEGER end

class B feature f do end end

class C feature f do end end

class D inherit

    A

         rename

             g as f            -- g was effective in A

         undefine

            f

         end

    B

         undefine f end                 -- f was effective in B

    C

        -- C also has an effective feature f , which will serve as

        -- implementation for the result of the join.

feature
    d_feature do end
end
"""

json_ast, stderr = run_eiffel_parser(eiffel_code, "build/eiffelp.exe")
if stderr:
    print(stderr, file=sys.stderr)
    sys.exit(1)

dict_ast = json.loads(json_ast)
classes = make_ast(dict_ast)

process_stage0(classes)
print(analyze_inheritance(classes[4]))
