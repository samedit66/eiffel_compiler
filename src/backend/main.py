import json

from tree.class_decl.make import make_class_decl
from execute import run_eiffel_parser



eiffel_code = """
class КВАДРАТ

inherit
    ПРЯМОУГОЛЬНИК
    redefine
        плошадь
    end

feature
    площадь
    do
        print ("Площадь!")
    end

    λ
    do
    end
end

"""

json_ast, stderr = run_eiffel_parser(eiffel_code, "build/eiffelp.exe")
print(json_ast)
print(stderr)
dict_ast = json.loads(json_ast)

class_decl = make_class_decl(dict_ast["classes"][0])
print(class_decl)
