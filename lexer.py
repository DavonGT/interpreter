import re
#
TOKEN_SPEC = [
    ("NUMBER",      r"\d+"),
    ("IDENTIFIER",  r"[a-zA-Z_]\w*"),
    ("ASSIGN",      r"="),
    ("OP",          r"[+\-*/]"),
    ("IF",          r"if"),
    ("ELIF",        r"elif"),
    ("ELSE",        r"else"),
    ("WHILE",       r"while"),
    ("FOR",         r"for"),
    ("IN",          r"in"),
    ("DEF",         r"def"),
    ("LPAREN",      r"\("),
    ("RPAREN",      r"\)"),
    ("COLON",       r":"),
    ("COMMA",       r","),
    ("SEMICOLON",   r";"),         # <-- Added for multiple statements
    ("NEWLINE",     r"\n"),        # <-- Ensure newlines are recognized
    ("SKIP",        r"[ \t]+"),
    ("MISMATCH",    r"."),
]


class Lexer:
    def __init__(self, code):
        self.tokens = []
        self.code = code
        self.indent_stack = [0]
        self.keywords = {
            "def": "DEF",
            "if": "IF",
            "elif": "ELIF",
            "else": "ELSE",
            "while": "WHILE",
            "for": "FOR",
            "in": "IN",
            "return": "RETURN",
        }
        self.tokenize()

    def tokenize(self):
        lines = self.code.splitlines()
        for line in lines:
            indent = len(line) - len(line.lstrip())
            if indent > self.indent_stack[-1]:
                self.tokens.append(("INDENT", indent))
                self.indent_stack.append(indent)
            while indent < self.indent_stack[-1]:
                self.tokens.append(("DEDENT", self.indent_stack.pop()))

            for match in re.finditer("|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC), line):
                kind = match.lastgroup
                value = match.group()
                # Check if it's an IDENTIFIER and if it is a keyword
                if kind == "IDENTIFIER" and value in self.keywords:
                    kind = self.keywords[value]  # Change token type to corresponding keyword
                elif kind == "NUMBER":
                    value = int(value)
                elif kind == "SKIP":
                    continue
                elif kind == "MISMATCH":
                    raise SyntaxError(f"Unexpected character: {value}")
                self.tokens.append((kind, value))
            self.tokens.append(("NEWLINE", "\n"))

        while len(self.indent_stack) > 1:
            self.tokens.append(("DEDENT", self.indent_stack.pop()))

    def next_token(self):
        return self.tokens.pop(0) if self.tokens else ("EOF", "EOF")


# Example Usage:
#code = """
#x = 10
#def print():
#    return 20
#"""
#lexer = Lexer(code)
#print(lexer.tokens)

