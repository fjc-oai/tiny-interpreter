from typing import Any
from interface import Expr, Visitor
from expr import BinaryExpr, UnaryExpr, LiteralExpr, GroupingExpr
from tok import TokenType
import logging

logger = logging.getLogger(__name__)


class Interpreter(Visitor):

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
                assert isinstance(
                    left_val, float | str
                ), f"BinaryExpr: {left_val} is not a number or string"
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


def test_interpreter():
    from scanner import Scanner
    from parser import Parser

    sources = ["1 + 2 * 3", "(1+2)  * 3", "1---1"]

    for source in sources:
        tokens = Scanner(source).scan()
        expr = Parser(tokens).parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expr)
        expected = eval(source)
        assert result == expected, f"Interpreter: {source} = {result} != {expected}"
        logger.info(f"Interpreter: {source} = {result}")


if __name__ == "__main__":
    test_interpreter()
