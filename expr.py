from dataclasses import dataclass
from typing import Any
from scanner import Token
from interface import Expr, Visitor


@dataclass
class LiteralExpr(Expr):
    value: Token

    def accept(self, visitor: Visitor):
        return visitor.visit_literal_expr(self)


@dataclass
class UnaryExpr(Expr):
    right: Expr
    op: Token

    def accept(self, visitor: Visitor):
        return visitor.visit_unary_expr(self)


@dataclass
class BinaryExpr(Expr):
    left: Expr
    right: Expr
    op: Token

    def accept(self, visitor: Visitor):
        return visitor.visit_binary_expr(self)


@dataclass
class GroupingExpr(Expr):
    expr: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_grouping_expr(self)
