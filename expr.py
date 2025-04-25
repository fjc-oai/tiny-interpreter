from dataclasses import dataclass
from typing import Any
from scanner import Token
from interface import Expr, Visitor


########################################################
# Basic expressions
########################################################
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


########################################################
# Statements
########################################################
@dataclass
class PrintStmt(Expr):
    expr: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_print_stmt(self)


@dataclass
class DeclStmt(Expr):
    name: Token
    expr: Expr | None

    def accept(self, visitor: Visitor):
        return visitor.visit_decl_stmt(self)


@dataclass
class AssignStmt(Expr):
    name: Token
    expr: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_assign_stmt(self)


@dataclass
class Block(Expr):
    exprs: list[Expr]

    def accept(self, visitor: Visitor):
        return visitor.visit_block(self)


@dataclass
class Program(Expr):
    exprs: list[Expr]

    def accept(self, visitor: Visitor):
        return visitor.visit_program(self)


########################################################
# Control flow
########################################################

@dataclass
class IfStmt(Expr):
    condition: Expr
    then_branch: Expr
    else_branch: Expr | None

    def accept(self, visitor: Visitor):
        return visitor.visit_if_stmt(self)


@dataclass
class WhileStmt(Expr):
    condition: Expr
    body: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_while_stmt(self)