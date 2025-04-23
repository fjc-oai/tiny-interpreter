from interface import Visitor, Expr
from scanner import Token, TokenType
from expr import BinaryExpr, GroupingExpr, UnaryExpr, LiteralExpr


class ExprPrinter(Visitor):
    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def visit_binary_expr(self, expr: BinaryExpr):
        left = self.print(expr.left)
        right = self.print(expr.right)
        res = f"({expr.op.token_type} {left} {right})"
        return res

    def visit_unary_expr(self, expr: "UnaryExpr"):
        right = self.print(expr.right)
        res = f"({expr.op.token_type} {right})"
        return res

    def visit_literal_expr(self, expr: "LiteralExpr"):
        return f"{expr.value.lexeme}"

    def visit_grouping_expr(self, expr: "GroupingExpr"):
        return f"({self.print(expr.expr)})"


def test_ast_printer():
    3 + (-5)
    literal_expr = LiteralExpr(value=Token(TokenType.NUMBER, "5", 5, 0))
    unary_expr = UnaryExpr(right=literal_expr, op=Token(TokenType.MINUS, "", "", 0))
    literal_expr2 = LiteralExpr(value=Token(TokenType.NUMBER, "3", 3, 0))
    binary_expr = BinaryExpr(
        left=literal_expr2,
        right=unary_expr,
        op=Token(TokenType.PLUS, "", "", 0),
    )

    printer = ExprPrinter()
    print(f"{printer.print(binary_expr)}")


def main():
    test_ast_printer()


if __name__ == "__main__":
    main()
