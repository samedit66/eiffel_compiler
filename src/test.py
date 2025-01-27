from backend.semantic.stage2.types import *
from backend.semantic.stage2.expr_type import *


def test_constant_types():
    type_scope = TypeScope(defined_types={
        "INTEGER": TypedClass("INTEGER"),
        "REAL": TypedClass("REAL"),
        "CHARACTER": TypedClass("CHARACTER"),
        "STRING": TypedClass("STRING"),
        "BOOLEAN": TypedClass("BOOLEAN"),
        "Void": TypedClass("Void"),
    })

    assert type_of_expr(IntegerConst(location=None, value=42), type_scope, None) == type_scope.find("INTEGER")
    assert type_of_expr(RealConst(location=None, value=3.14), type_scope, None) == type_scope.find("REAL")
    assert type_of_expr(CharacterConst(location=None, value='a'), type_scope, None) == type_scope.find("CHARACTER")
    assert type_of_expr(StringConst(location=None, value="hello"), type_scope, None) == type_scope.find("STRING")
    assert type_of_expr(BoolConst(location=None, value=True), type_scope, None) == type_scope.find("BOOLEAN")
    assert type_of_expr(VoidConst(location=None), type_scope, None) == type_scope.find("Void")


def test_feature_call():
    type_scope = TypeScope({
        "INTEGER": TypedClass("INTEGER"),
        "BOOLEAN": TypedClass("BOOLEAN"),
    })

    caller = TypedClass("MyClass")
    local_scope = Scope({
        "some_feature": TypedMethod(
            name="some_feature",
            type_of=TypedClass("INTEGER"),
            parameters=[]
        ),
    })

    in_method = TypedMethod(
        name="test_method",
        type_of=TypedClass("VOID"),
        local_scope=local_scope,
    )

    expr = FeatureCall(
        feature_name="some_feature",
        arguments=[],
    )

    assert type_of_expr(expr, type_scope, caller, in_method) == type_scope.find("INTEGER")
