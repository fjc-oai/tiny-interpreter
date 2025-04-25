from dataclasses import dataclass
from enum import Enum
from typing import Any


class TokenType(Enum):
    LEFT_PAREN = "()"
    RIGHT_PAREN = ")"
    LEFT_BRACE = "["
    RIGHT_BRACE = "]"
    COMMA = ","
    DOT = "."
    MINUS = "-"
    PLUS = "+"
    SEMICOLON = ";"
    SLASH = "/"
    STAR = "*"
    # One or two character tokens.
    BANG = "!"
    BANG_EQUAL = "!="
    EQUAL = "="
    EQUAL_EQUAL = "=="
    GREATER = ">"
    GREATER_EQUAL = ">="
    LESS = "<"
    LESS_EQUAL = "<="
    # Literals.
    IDENTIFIER = "id"
    STRING = "str"
    NUMBER = "num"
    # Keywords.
    AND = "and"
    CLASS = "class"
    ELSE = "else"
    FALSE = "false"
    FUNC = "def"
    FOR = "for"
    IF = "if"
    NIL = "nil"
    OR = "or"
    PRINT = "print"
    RETURN = "ret"
    SUPER = "super"
    THIS = "this"
    TRUE = "true"
    VAR = "var"
    WHILE = "while"
    EOF = "eof"
    DEBUG = "debug"
    DISCARD = "discard"  # e.g. comment, space, etc


KEYWORDS: dict[str, TokenType] = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "def": TokenType.FUNC,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
    "debug": TokenType.DEBUG,
}

@dataclass
class Token:
    token_type: TokenType
    lexeme: str
    literal: Any
    lineno: int

    def __str__(self) -> str:
        return f"[{self.token_type}] {self.lexeme=}, {self.literal=} {self.lineno=}"