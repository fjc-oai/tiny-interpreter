from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from expr import (
        BinaryExpr,
        UnaryExpr,
        LiteralExpr,
        GroupingExpr,
        DeclStmt,
        PrintStmt,
        AssignStmt,
        Block,
        Program,
        IfStmt,
        WhileStmt,
        ForStmt,
    )

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

    def visit_print_stmt(self, stmt: "PrintStmt"):
        pass

    def visit_decl_stmt(self, stmt: "DeclStmt"):
        pass

    def visit_assign_stmt(self, stmt: "AssignStmt"):
        pass

    def visit_block(self, block: "Block"):
        pass

    def visit_program(self, program: "Program"):
        pass

    def visit_if_stmt(self, stmt: "IfStmt"):
        pass

    def visit_while_stmt(self, stmt: "WhileStmt"):
        pass

    def visit_for_stmt(self, stmt: "ForStmt"):
        pass
