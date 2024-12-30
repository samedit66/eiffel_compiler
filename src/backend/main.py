from pathlib import Path
import json
from pprint import pprint as pp

from execute import run_eiffel_parser
from tree.class_decl import ClassDecl


eiffel_code = """
class SQUARE
    inherit RECTANGLE
        rename height as side, width as side
    end

feature
    area: REAL then side * side end

feature {NONE}

    fuck_that_shit, suck (a, b, c: POINT; d, e: INTEGER)
    require
        True; False; True;
    do
        a := if a > b then c elseif a < u then 41 else 12421 end;
    end

feature {A, B, C}

    constant: INTEGER = 10
end
"""

program_dict = json.loads(
    run_eiffel_parser(eiffel_code, "build\\eiffelp.exe")[0]
)

print(ClassDecl.from_dict(program_dict["classes"][0]))