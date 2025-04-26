from dataclasses import dataclass
import time
from typing import TYPE_CHECKING, Any, Callable

from interface import Expr
from tok import Token

if TYPE_CHECKING:
    from interpreter import Interpreter


@dataclass
class FuncBase:
    name: str
    params: list[str]

    def __call__(self, interpreter: "Interpreter") -> Any:
        pass


@dataclass
class Func(FuncBase):
    body: Expr

    def __call__(self, interpreter: "Interpreter") -> Any:
        return interpreter.interpret(self.body)


@dataclass
class NativeFunc(FuncBase):
    func: Callable

    def __call__(self, interpreter: "Interpreter") -> Any:
        kwargs = {}
        for param in self.params:
            kwargs[param] = interpreter._state.get(param)
        return self.func(interpreter, **kwargs)


def build_native_func_time() -> NativeFunc:
    def run_time(_: "Interpreter") -> int:
        return time.time()

    return NativeFunc(name="time", params=[], func=run_time)


def build_native_func_sleep() -> NativeFunc:
    def run_sleep(_: "Interpreter", seconds: int) -> None:
        time.sleep(seconds)

    return NativeFunc(name="sleep", params=["seconds"], func=run_sleep)
