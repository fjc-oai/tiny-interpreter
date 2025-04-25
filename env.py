from __future__ import annotations
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any

LookupTable = dict[str, Any]


@dataclass
class Env:
    lookup_tables: list[LookupTable]

    @contextmanager
    def block_scope(self):
        self.lookup_tables.append(LookupTable())
        yield
        self.lookup_tables.pop()

    def define(self, name: str, value: Any | None = None):
        cur_lookup_table = self.lookup_tables[-1]
        assert name not in cur_lookup_table, f"Variable already defined: {name}"
        cur_lookup_table[name] = value

    def assign(self, name: str, value: Any):
        for lookup_table in reversed(self.lookup_tables):
            if name in lookup_table:
                lookup_table[name] = value
                return
        raise ValueError(f"Undefined variable: {name}")

    def get(self, name: str) -> Any:
        for lookup_table in reversed(self.lookup_tables):
            if name in lookup_table:
                return lookup_table[name]
        raise ValueError(f"Undefined variable: {name}")


@dataclass
class State:
    env_list: list[Env] = field(init=False)

    def __post_init__(self):
        self.env_list = [Env(lookup_tables=[LookupTable()])]

    @contextmanager
    def block_scope(self):
        env = self.env_list[-1]
        with env.block_scope():
            yield

    def define(self, name: str, value: Any | None = None):
        env = self.env_list[-1]
        env.define(name, value)

    def assign(self, name: str, value: Any):
        env = self.env_list[-1]
        env.assign(name, value)

    def get(self, name: str) -> Any:
        env = self.env_list[-1]
        return env.get(name)

    @contextmanager
    def func_scope(self, args: dict[str, Any]):
        cur_env = self.env_list[-1]
        cur_global_vars = cur_env.lookup_tables[0]
        new_env = Env(lookup_tables=[cur_global_vars.copy()])
        new_env.lookup_tables.append(LookupTable())
        for k, v in args.items():
            new_env.define(k, v)
        self.env_list.append(new_env)
        yield
        self.env_list.pop()
