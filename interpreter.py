from typing import Any
from env import Environment
from interface import Expr, Visitor
from expr import (
    AssignStmt,
    BinaryExpr,
    Block,
    DeclStmt,
    PrintStmt,
    Program,
    UnaryExpr,
    LiteralExpr,
    GroupingExpr,
)
from tok import TokenType
import logging

from utils import color_print

logger = logging.getLogger(__name__)


class Interpreter(Visitor):
    def __init__(self):
        self._env = Environment()

    def interpret(self, expr: Expr) -> Any:
        return expr.accept(self)

    def visit_literal_expr(self, expr: "LiteralExpr"):
        accepted_types = [
            TokenType.NUMBER,
            TokenType.STRING,
            TokenType.TRUE,
            TokenType.FALSE,
            TokenType.NIL,
            TokenType.IDENTIFIER,
        ]
        token = expr.value
        assert (
            token.token_type in accepted_types
        ), f"LiteralExpr: {token.token_type} is not accepted"
        if token.token_type == TokenType.IDENTIFIER:
            return self._env.get(token.lexeme)
        else:
            return token.literal

    def visit_unary_expr(self, expr: "UnaryExpr"):
        accepted_types = [TokenType.MINUS, TokenType.BANG]
        token = expr.op
        assert (
            token.token_type in accepted_types
        ), f"UnaryExpr: {token.token_type} is not accepted"
        val = self.interpret(expr.right)
        match token.token_type:
            case TokenType.MINUS:
                assert isinstance(val, float), f"UnaryExpr: {val} is not a number"
                return -val
            case TokenType.BANG:
                assert isinstance(val, bool), f"UnaryExpr: {val} is not a boolean"
                return not val

    def visit_binary_expr(self, expr: "BinaryExpr"):
        accepted_types = [
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.SLASH,
            TokenType.STAR,
        ]
        token = expr.op
        assert (
            token.token_type in accepted_types
        ), f"BinaryExpr: {token.token_type} is not accepted"
        left_val = self.interpret(expr.left)
        right_val = self.interpret(expr.right)
        match token.token_type:
            case TokenType.PLUS:
                assert type(left_val) == type(
                    right_val
                ), f"BinaryExpr: {left_val} and {right_val} are not the same type"
                try:
                    assert isinstance(
                        left_val, float | str
                    ), f"BinaryExpr: {left_val} is not a number or string"
                except AssertionError as e:
                    breakpoint()
                return left_val + right_val
            case TokenType.MINUS:
                assert isinstance(
                    left_val, float
                ), f"BinaryExpr: {left_val} is not a number"
                assert isinstance(
                    right_val, float
                ), f"BinaryExpr: {right_val} is not a number"
                return left_val - right_val
            case TokenType.SLASH:
                assert isinstance(
                    left_val, float
                ), f"BinaryExpr: {left_val} is not a number"
                assert isinstance(
                    right_val, float
                ), f"BinaryExpr: {right_val} is not a number"
                return left_val / right_val
            case TokenType.STAR:
                assert isinstance(
                    left_val, float
                ), f"BinaryExpr: {left_val} is not a number"
                assert isinstance(
                    right_val, float
                ), f"BinaryExpr: {right_val} is not a number"
                return left_val * right_val
        assert False, f"BinaryExpr: {token.token_type} is not handled"

    def visit_grouping_expr(self, expr: "GroupingExpr"):
        return self.interpret(expr.expr)

    def visit_print_stmt(self, stmt: "PrintStmt"):
        val = self.interpret(stmt.expr)
        str = f"[interpreter] {val}"
        str = color_print(str, "yellow")
        print(str)

    def visit_decl_stmt(self, stmt: "DeclStmt"):
        if stmt.expr is None:
            val = None
        else:
            val = self.interpret(stmt.expr)
        self._env.define(stmt.name.lexeme, val)

    def visit_assign_stmt(self, stmt: "AssignStmt"):
        val = self.interpret(stmt.expr)
        self._env.assign(stmt.name.lexeme, val)

    def visit_block(self, block: "Block"):
        with self._env.scope():
            for stmt in block.exprs:
                self.interpret(stmt)

    def visit_program(self, program: "Program"):
        for stmt in program.exprs:
            self.interpret(stmt)


def test_interpreter():
    from scanner import Scanner
    from parser import Parser

    sources = [
        """
        var a = 1;
        var b = 2;
        print a + b;
        {
            var c = 8;
            print c;
        }
        {
            var a = 4;
            print a + b;
        }
        print a + 2 * 3;
        print (a + 2) * 3;
    """,
    ]

    for source in sources:
        print("-" * 80)
        print(f"Testing source: {source}")
        tokens = Scanner(source).scan()
        expr = Parser(tokens).parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expr)


if __name__ == "__main__":
    test_interpreter()
