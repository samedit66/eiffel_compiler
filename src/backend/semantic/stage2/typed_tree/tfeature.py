from dataclasses import dataclass, field

from .tables import Type
from .texpr import TypedExpr
from .tstmt import TypedStatement


@dataclass(kw_only=True)
class TypedFeature:
    name: str
    clients: list[Type]
    type_of: Type


@dataclass(kw_only=True)
class TypedConstant(TypedFeature):
    value: TypedExpr


@dataclass(kw_only=True)
class TypedField(TypedFeature):
    pass


@dataclass(kw_only=True)
class TypedLocal(TypedFeature):
    pass


@dataclass(match_args=True, kw_only=True)
class TypedCondition:
    condition: TypedExpr
    tag: str | None = None


@dataclass(kw_only=True)
class TypedBaseMethod(TypedFeature):
    parameters: list[TypedLocal] = field(default_factory=list)
    require: list[TypedCondition] = field(default_factory=list)
    ensure: list[TypedCondition] = field(default_factory=list)


@dataclass
class TypedMethod(TypedBaseMethod):
    is_deferred: bool
    do: list[TypedStatement] = field(default_factory=list)
    variables: list[TypedLocal] = field(default_factory=list)


@dataclass
class TypedExternalMethod(TypedBaseMethod):
    language: str
    alias: str
