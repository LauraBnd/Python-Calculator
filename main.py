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
            tokens.pop(0) 
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

def create_calculator():
    def append_to_expression(value):
        entry_var.set(entry_var.get() + value)

    def clear_entry():
        entry_var.set("")

    def calculate():
        expression = entry_var.get()
        try:
            lexer = Lexer(expression)
            tokens = lexer.tokenize()
            result = evaluate(tokens)
            entry_var.set(str(result))
        except Exception as e:
            entry_var.set(f"Error: {e}")

    root = tk.Tk()
    root.title("Calculator")
    root.configure(bg="#e9f7f5")

    entry_var = tk.StringVar()
    entry = tk.Entry(root, textvariable=entry_var, font=("Arial", 24), bd=10, insertwidth=4, justify="right")
    entry.grid(row=0, column=0, columnspan=5, sticky="nsew")

    for i in range(6):
        root.grid_rowconfigure(i, weight=1)
    for j in range(5):
        root.grid_columnconfigure(j, weight=1)

    buttons = [
        ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("=", 1, 3), ("C", 1, 4),
        ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("+", 2, 3), ("-", 2, 4),
        ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("*", 3, 3), ("/", 3, 4),
        ("0", 4, 0), (".", 4, 1), ("(", 4, 2), (")", 4, 3), ("^", 4, 4),
        ("sin", 5, 0), ("cos", 5, 1), ("tan", 5, 2), ("log", 5, 3), ("sqrt", 5, 4),
    ]

    for (text, row, col) in buttons:
        if text == "C":
            action = clear_entry
            button_bg = "#7CBFB2"
        elif text == "=":
            action = calculate
            button_bg = "#7CBFB2"
        else:
            action = lambda t=text: append_to_expression(t)
            button_bg = "#c5e7e1"

        button = tk.Button(root, text=text, font=("Arial", 18), command=action,
                           bg=button_bg, fg="#000000")
        button.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

    root.mainloop()


if __name__ == "__main__":
    create_calculator()
