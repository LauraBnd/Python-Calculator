import tkinter as tk
import math
import re

# Lexer implementation
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



if __name__ == "__main__":
    create_calculator()
