from scanner import Token, TokenType
import logging

logger = logging.getLogger(__name__)

from expr import (
    AssignStmt,
    Block,
    DeclStmt,
    Expr,
    BinaryExpr,
    ForStmt,
    FuncCall,
    GroupingExpr,
    IfStmt,
    LiteralExpr,
    PrintStmt,
    Program,
    ReturnStmt,
    UnaryExpr,
    WhileStmt,
    FuncDecl,
)


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self._cur = 0
        self._tokens = tokens

    def parse(self) -> Expr:
        return self._program()

    def _peek(self, offset: int = 0) -> Token:
        assert not self._is_at_end()
        assert self._cur + offset < len(self._tokens)
        return self._tokens[self._cur + offset]

    def _is_at_end(self) -> bool:
        return self._cur >= len(self._tokens)

    def _advance(self, expected_token_type: TokenType | None = None) -> Token:
        assert not self._is_at_end()
        token = self._tokens[self._cur]
        self._cur += 1
        if expected_token_type is not None:
            assert (
                token.token_type == expected_token_type
            ), f"Expected {expected_token_type} but got {token.token_type}"
        return token

    def _expression(self) -> Expr:
        return self._or()

    def _or(self) -> Expr:
        expr = self._and()

        while not self._is_at_end() and self._peek().token_type == TokenType.OR:
            op = self._advance(TokenType.OR)
            right = self._and()
            expr = BinaryExpr(left=expr, right=right, op=op)

        return expr

    def _and(self) -> Expr:
        expr = self._equality()

        while not self._is_at_end() and self._peek().token_type == TokenType.AND:
            op = self._advance(TokenType.AND)
            right = self._equality()
            expr = BinaryExpr(left=expr, right=right, op=op)

        return expr

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

        return self._func_call()

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
                not self._is_at_end()
                and self._advance().token_type == TokenType.RIGHT_PAREN
            ), f"Expected ')' after expression"

            return GroupingExpr(expr)

        raise ValueError(f"Unexpected token {self._peek()}")

    def _program(self) -> Expr:
        exprs = []
        while not self._is_at_end() and self._peek().token_type != TokenType.EOF:
            exprs.append(self._statement())
        return Program(exprs)

    def _statement(self) -> Expr:
        if self._peek().token_type == TokenType.PRINT:
            return self._print_stmt()
        elif self._peek().token_type == TokenType.VAR:
            return self._decl_stmt()
        elif self._peek().token_type == TokenType.FUNC:
            return self._func_decl_stmt()
        elif self._peek().token_type == TokenType.LEFT_BRACE:
            return self._block_stmt()
        elif self._peek().token_type == TokenType.IF:
            return self._if_stmt()
        elif self._peek().token_type == TokenType.WHILE:
            return self._while_stmt()
        elif self._peek().token_type == TokenType.FOR:
            return self._for_stmt()
        elif self._peek().token_type == TokenType.RETURN:
            return self._return_stmt()
        else:
            if (
                self._peek().token_type == TokenType.IDENTIFIER
                and self._peek(1).token_type == TokenType.EQUAL
            ):
                return self._assign_stmt()
            else:
                expr = self._expression()
                self._advance(TokenType.SEMICOLON)
                return expr

    def _print_stmt(self) -> Expr:
        self._advance(TokenType.PRINT)
        expr = self._expression()
        self._advance(TokenType.SEMICOLON)
        return PrintStmt(expr)

    def _decl_stmt(self) -> Expr:
        self._advance(TokenType.VAR)
        name = self._advance(TokenType.IDENTIFIER)
        if not self._is_at_end() and self._peek().token_type == TokenType.EQUAL:
            self._advance()
            expr = self._expression()
        else:
            expr = None
        self._advance(TokenType.SEMICOLON)
        return DeclStmt(name=name, expr=expr)

    def _assign_stmt(self) -> Expr:
        name = self._advance(
            TokenType.IDENTIFIER
        )  # TODO: support more complex access, e.g. a.b.c
        self._advance(TokenType.EQUAL)
        expr = self._expression()
        self._advance(TokenType.SEMICOLON)
        return AssignStmt(name=name, expr=expr)

    def _block_stmt(self) -> Expr:
        self._advance(TokenType.LEFT_BRACE)
        exprs = []
        while (
            not self._is_at_end() and self._peek().token_type != TokenType.RIGHT_BRACE
        ):
            exprs.append(self._statement())
        self._advance(TokenType.RIGHT_BRACE)
        return Block(exprs)

    def _if_stmt(self) -> Expr:
        self._advance(TokenType.IF)
        condition = self._expression()
        then_branch = self._statement()
        else_branch = None
        if not self._is_at_end() and self._peek().token_type == TokenType.ELSE:
            self._advance(TokenType.ELSE)
            else_branch = self._statement()
        return IfStmt(
            condition=condition, then_branch=then_branch, else_branch=else_branch
        )

    def _while_stmt(self) -> Expr:
        self._advance(TokenType.WHILE)
        self._advance(TokenType.LEFT_PAREN)
        condition = self._expression()
        self._advance(TokenType.RIGHT_PAREN)
        body = self._statement()
        return WhileStmt(condition=condition, body=body)

    def _for_stmt(self) -> Expr:
        self._advance(TokenType.FOR)
        self._advance(TokenType.LEFT_PAREN)
        if self._peek().token_type == TokenType.VAR:
            init = self._decl_stmt()
        else:
            init = self._expression()
            self._advance(TokenType.SEMICOLON)
        condition = self._expression()
        self._advance(TokenType.SEMICOLON)
        update = self._assign_stmt()
        self._advance(TokenType.RIGHT_PAREN)
        body = self._statement()
        return ForStmt(init=init, condition=condition, update=update, body=body)

    def _func_decl_stmt(self) -> Expr:
        self._advance(TokenType.FUNC)
        name = self._advance(TokenType.IDENTIFIER)
        self._advance(TokenType.LEFT_PAREN)
        params = []
        while (
            not self._is_at_end() and self._peek().token_type != TokenType.RIGHT_PAREN
        ):
            params.append(self._advance(TokenType.IDENTIFIER))
            if self._peek().token_type == TokenType.COMMA:
                self._advance(TokenType.COMMA)
        self._advance(TokenType.RIGHT_PAREN)
        body = self._block_stmt()
        return FuncDecl(name=name, params=params, body=body)

    def _func_call(self) -> Expr:
        if (
            self._peek().token_type == TokenType.IDENTIFIER
            and self._peek(1).token_type == TokenType.LEFT_PAREN
        ):  # TODO: support fn()()
            name = self._advance(TokenType.IDENTIFIER)
            self._advance(TokenType.LEFT_PAREN)
            args = []
            while (
                not self._is_at_end()
                and self._peek().token_type != TokenType.RIGHT_PAREN
            ):
                args.append(self._expression())
                if self._peek().token_type == TokenType.COMMA:
                    self._advance(TokenType.COMMA)
            self._advance(TokenType.RIGHT_PAREN)
            return FuncCall(name=name, args=args)
        return self._primary()

    def _return_stmt(self) -> Expr:
        self._advance(TokenType.RETURN)
        if not self._is_at_end() and self._peek().token_type != TokenType.SEMICOLON:
            expr = self._expression()
        else:
            expr = None
        self._advance(TokenType.SEMICOLON)
        return ReturnStmt(expr=expr)


def _test_expression(source: str) -> None:
    from scanner import Scanner

    tokens = Scanner(source).scan()
    for idx, token in enumerate(tokens):
        logger.debug(f"{idx}: {token}")

    parser = Parser(tokens)
    expr = parser._expression()
    print(f"{expr}")


def test_multiple_expressions():
    source = "a + 2 * 3"
    print("-" * 80)
    print(f"Testing multiple expressions: {source}")
    _test_expression(source)


def test_unary_operator():
    source = "---a"
    print("-" * 80)
    print(f"Testing unary operator: {source}")
    _test_expression(source)


def test_grouping():
    source = "(a + 2) * 3"
    print("-" * 80)
    print(f"Testing grouping: {source}")
    _test_expression(source)


def test_precedence():
    source = "a * 2 * 3 - b * 2"
    print("-" * 80)
    print(f"Testing precedence: {source}")
    _test_expression(source)


def _test_parser(source: str) -> None:
    from scanner import Scanner

    tokens = Scanner(source).scan()
    parser = Parser(tokens)
    expr = parser.parse()
    print(f"{expr}")


def test_program():
    source = """
    var a = 1;
    var b = 2;
    print a + b;
    {
        var c = 3;
        print c;
    }
    """
    print("-" * 80)
    print(f"Testing program: {source}")
    _test_parser(source)


def test_expression():
    test_multiple_expressions()
    test_unary_operator()
    test_grouping()
    test_precedence()


def test_parser():
    test_program()


if __name__ == "__main__":
    test_parser()
