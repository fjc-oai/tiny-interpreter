from typing import Any
from env import Environment
from interface import Expr, Visitor
from expr import (
    AssignStmt,
    BinaryExpr,
    Block,
    DeclStmt,
    IfStmt,
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

    def _handle_math_op(self, expr: "BinaryExpr"):
        token = expr.op
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

    def _handle_logic_op(self, expr: "BinaryExpr"):
        left_val = self.interpret(expr.left)
        right_val = self.interpret(expr.right)
        match expr.op.token_type:
            case TokenType.EQUAL_EQUAL:
                return left_val == right_val
            case TokenType.BANG_EQUAL:
                return left_val != right_val
            case TokenType.GREATER:
                return left_val > right_val
            case TokenType.GREATER_EQUAL:
                return left_val >= right_val
            case TokenType.LESS:
                return left_val < right_val
            case TokenType.LESS_EQUAL:
                return left_val <= right_val
            case _:
                assert False, f"BinaryExpr: {expr.op.token_type} is not handled"

    def _handle_and_or_op(self, expr: "BinaryExpr"):
        op = expr.op
        if op.token_type == TokenType.AND:
            left_val = self.interpret(expr.left)
            if left_val:
                return self.interpret(expr.right)
            else:
                return False
        elif op.token_type == TokenType.OR:
            left_val = self.interpret(expr.left)
            if left_val:
                return left_val
            else:
                return self.interpret(expr.right)
        assert False, f"BinaryExpr: {expr.op.token_type} is not handled"

    def visit_binary_expr(self, expr: "BinaryExpr"):
        math_ops = [
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.SLASH,
            TokenType.STAR,
        ]
        logic_ops = [
            TokenType.EQUAL_EQUAL,
            TokenType.BANG_EQUAL,
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ]
        and_or_ops = [
            TokenType.AND,
            TokenType.OR,
        ]

        if expr.op.token_type in math_ops:
            return self._handle_math_op(expr)
        elif expr.op.token_type in logic_ops:
            return self._handle_logic_op(expr)
        elif expr.op.token_type in and_or_ops:
            return self._handle_and_or_op(expr)
        assert False, f"BinaryExpr: {expr.op.token_type} is not handled"

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

    def visit_if_stmt(self, stmt: "IfStmt"):
        condition = self.interpret(stmt.condition)
        if condition:
            self.interpret(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.interpret(stmt.else_branch)


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
        """
        var a = 1;
        var b = 2;
        if a > b {
            print "a is greater than b";
        } else {
            print "a is less than or equal to b";
        }
        if a > b or a < b {
            print "a is greater than b or less than b";
        }
        if a > b and a < b {
            print "a is greater than b and less than b";
        }
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
