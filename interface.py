from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from expr import BinaryExpr, UnaryExpr, LiteralExpr, GroupingExpr

import logging
import config_logging

logger = logging.getLogger(__name__)


@dataclass
class Expr:
    def __post_init__(self):
        logger.debug(f"Constructing {self.__class__.__name__}")

    def accept(self, visitor: "Visitor"):
        pass

    def __str__(self) -> str:
        from printer import ExprPrinter

        printer = ExprPrinter()
        return printer.print(self)


class Visitor:
    def visit_binary_expr(self, expr: "BinaryExpr"):
        pass

    def visit_unary_expr(self, expr: "UnaryExpr"):
        pass

    def visit_literal_expr(self, expr: "LiteralExpr"):
        pass

    def visit_grouping_expr(self, expr: "GroupingExpr"):
        pass
