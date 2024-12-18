import tkinter as tk
import math
import re

class Lexer:
    TOKENS = {
        r'\+': 'PLUS',
        r'\-': 'MINUS',
        r'\*': 'MULTIPLY',
        r'/': 'DIVIDE',
        r'\^': 'POWER',
        r'sqrt': 'SQRT',
        r'log': 'LOG',
        r'sin': 'SIN',
        r'cos': 'COS',
        r'tan': 'TAN',
        r'\(': 'LPAREN',
        r'\)': 'RPAREN',
        r'[0-9]+(\.[0-9]+)?': 'NUMBER'
    }

    def __init__(self, expression):
        self.expression = expression.replace(" ", "")
        self.tokens = []

    def tokenize(self):
        pos = 0
        while pos < len(self.expression):
            match = None
            for pattern, token_type in self.TOKENS.items():
                regex = re.compile(pattern)
                match = regex.match(self.expression, pos)
                if match:
                    value = match.group(0)
                    self.tokens.append((token_type, value))
                    pos = match.end()
                    break
            if not match:
                raise ValueError(f"Unexpected character at position {pos}: {self.expression[pos]}")
        return self.tokens


def evaluate(tokens):
    def parse_expression():
        value = parse_term()
        while tokens and tokens[0][0] in ('PLUS', 'MINUS'):
            token = tokens.pop(0)
            if token[0] == 'PLUS':
                value += parse_term()
            elif token[0] == 'MINUS':
                value -= parse_term()
        return value

    def parse_term():
        value = parse_exponent()
        while tokens and tokens[0][0] in ('MULTIPLY', 'DIVIDE'):
            token = tokens.pop(0)
            if token[0] == 'MULTIPLY':
                value *= parse_exponent()
            elif token[0] == 'DIVIDE':
                value /= parse_exponent()
        return value

    def parse_exponent():
        value = parse_factor()
        while tokens and tokens[0][0] == 'POWER':
            tokens.pop(0)  # Remove the POWER token
            value **= parse_factor()
        return value

    def parse_factor():
        token = tokens.pop(0)
        if token[0] == 'NUMBER':
            return float(token[1])
        elif token[0] == 'LPAREN':
            value = parse_expression()
            if tokens.pop(0)[0] != 'RPAREN':
                raise ValueError("Mismatched parentheses")
            return value
        elif token[0] == 'MINUS':
            return -parse_factor()
        elif token[0] == 'SQRT':
            return math.sqrt(parse_factor())
        elif token[0] == 'LOG':
            return math.log(parse_factor())
        elif token[0] == 'SIN':
            return math.sin(parse_factor())
        elif token[0] == 'COS':
            return math.cos(parse_factor())
        elif token[0] == 'TAN':
            return math.tan(parse_factor())
        else:
            raise ValueError(f"Unexpected token: {token}")

    return parse_expression()

