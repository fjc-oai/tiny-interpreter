from dataclasses import dataclass
from typing import Any, Callable

from interface import Expr
from tok import Token


@dataclass
class FuncBase:
    name: str
    params: list[Token]

    def __call__(self, *args: Any) -> Any:
        pass


@dataclass
class Func(FuncBase):
    body: Expr
