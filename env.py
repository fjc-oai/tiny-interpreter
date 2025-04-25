from __future__ import annotations
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any


@dataclass
class LookupTable:
    vars: dict[str, Any] = field(default_factory=dict)


@dataclass
class Environment:
    _lookup_tables: list[LookupTable] = field(init=False)

    def __post_init__(self):
        self._lookup_tables = [LookupTable()]

    @contextmanager
    def scope(self):
        self._lookup_tables.append(LookupTable())
        yield
        self._lookup_tables.pop()

    def define(self, name: str, value: Any | None = None):
        assert (
            name not in self._lookup_tables[-1].vars
        ), f"Variable already defined: {name}"
        self._lookup_tables[-1].vars[name] = value

    def assign(self, name: str, value: Any):
        for lookup_table in reversed(self._lookup_tables):
            if name in lookup_table.vars:
                lookup_table.vars[name] = value
                return
        raise ValueError(f"Undefined variable: {name}")

    def get(self, name: str) -> Any:
        for lookup_table in reversed(self._lookup_tables):
            if name in lookup_table.vars:
                return lookup_table.vars[name]
        raise ValueError(f"Undefined variable: {name}")
