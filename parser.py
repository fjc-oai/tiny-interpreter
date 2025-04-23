from scanner import Token, TokenType
from expr import Expr, BinaryExpr, GroupingExpr, LiteralExpr, UnaryExpr


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self._cur = 0
        self._tokens = tokens

    def parse(self) -> Expr:
        return self._expression()

    def _peek(self) -> Token:
        assert not self._is_at_end()
        return self._tokens[self._cur]

    def _is_at_end(self) -> bool:
        return self._cur >= len(self._tokens)

    def _advance(self) -> Token:
        assert not self._is_at_end()
        token = self._tokens[self._cur]
        self._cur += 1
        return token

    def _expression(self) -> Expr:
        return self._equality()

    def _equality(self) -> Expr:
        expr = self._comparison()

        while not self._is_at_end() and self._peek().token_type in (
            TokenType.BANG_EQUAL,
            TokenType.EQUAL_EQUAL,
        ):
            op = self._advance()
            right = self._comparison()
            expr = BinaryExpr(left=expr, right=right, op=op)

        return expr

    def _comparison(self) -> Expr:
        expr = self._term()

        while not self._is_at_end() and self._peek().token_type in (
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            op = self._advance()
            right = self._term()
            expr = BinaryExpr(left=expr, right=right, op=op)

        return expr

    def _term(self) -> Expr:
        expr = self._factor()

        while not self._is_at_end() and self._peek().token_type in (
            TokenType.MINUS,
            TokenType.PLUS,
        ):
            op = self._advance()
            right = self._factor()
            expr = BinaryExpr(left=expr, right=right, op=op)

        return expr

    def _factor(self) -> Expr:
        expr = self._unary()

        while not self._is_at_end() and self._peek().token_type in (
            TokenType.SLASH,
            TokenType.STAR,
        ):
            op = self._advance()
            right = self._unary()
            expr = BinaryExpr(left=expr, right=right, op=op)

        return expr

    def _unary(self) -> Expr:
        if not self._is_at_end() and self._peek().token_type in (
            TokenType.BANG,
            TokenType.MINUS,
        ):
            op = self._advance()
            right = self._unary()
            return UnaryExpr(right=right, op=op)

        return self._primary()

    def _primary(self) -> Expr:
        primary_token_types = (
            TokenType.FALSE,
            TokenType.TRUE,
            TokenType.NIL,
            TokenType.NUMBER,
            TokenType.STRING,
            TokenType.IDENTIFIER,
        )
        if not self._is_at_end() and self._peek().token_type in primary_token_types:
            return LiteralExpr(value=self._advance())

        if not self._is_at_end() and self._peek().token_type == TokenType.LEFT_PAREN:
            self._advance()
            expr = self._expression()
            assert (
                not self._is_at_end() and self._advance().token_type == TokenType.RIGHT_PAREN
            ), f"Expected ')' after expression"

            return GroupingExpr(expr)

        raise ValueError(f"Unexpected token {self._peek()}")


def _test_parser(source: str) -> None:
    from scanner import Scanner

    tokens = Scanner(source).scan()
    for idx, token in enumerate(tokens):
        print(f"{idx}: {token}")

    parser = Parser(tokens)
    expr = parser.parse()
    print(f"{expr}")


def test_multiple_expressions():
    source = "a + 2 * 3"
    print("-" * 80)
    print(f"Testing multiple expressions: {source}")
    _test_parser(source)


def test_unary_operator():
    source = "---a"
    print("-" * 80)
    print(f"Testing unary operator: {source}")
    _test_parser(source)


def test_grouping():
    source = "(a + 2) * 3"
    print("-" * 80)
    print(f"Testing grouping: {source}")
    _test_parser(source)


def test_precedence():
    source = "a * 2 * 3 - b * 2"
    print("-" * 80)
    print(f"Testing precedence: {source}")
    _test_parser(source)


def main():
    test_multiple_expressions()
    test_unary_operator()
    test_grouping()
    test_precedence()


if __name__ == "__main__":
    main()
