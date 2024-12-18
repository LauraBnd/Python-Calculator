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

