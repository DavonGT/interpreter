TOKEN_SPEC = [
    ("NUMBER",      "0123456789"),
    ("IDENTIFIER",  "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"),
    ("ASSIGN",      "="),
    ("OP",          "+-*/"),
    ("IF",          "if"),
    ("ELIF",        "elif"),
    ("ELSE",        "else"),
    ("WHILE",       "while"),
    ("FOR",         "for"),
    ("IN",          "in"),
    ("DEF",         "def"),
    ("LPAREN",      "("),
    ("RPAREN",      ")"),
    ("COLON",       ":"),
    ("COMMA",       ","),
    ("SEMICOLON",   ";"),
    ("NEWLINE",     "\n"),
    ("SKIP",        " \t"),
    ("MISMATCH",    ""),
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

            index = 0
            while index < len(line):
                char = line[index]

                if char in " \t":
                    index += 1
                    continue

                for kind, pattern in TOKEN_SPEC:
                    if kind == "NUMBER" and char in pattern:
                        value = ''
                        while index < len(line) and line[index] in pattern:
                            value += line[index]
                            index += 1
                        self.tokens.append((kind, int(value)))
                        break
                    elif kind == "IDENTIFIER" and char in pattern:
                        value = ''
                        while index < len(line) and (line[index] in pattern or line[index].isdigit()):
                            value += line[index]
                            index += 1
                        if value in self.keywords:
                            self.tokens.append((self.keywords[value], value))
                        else:
                            self.tokens.append((kind, value))
                        break
                    elif char == pattern:
                        self.tokens.append((kind, char))
                        index += 1
                        break
                    elif kind == "IF" and line[index:index+2] == "if":
                        self.tokens.append((kind, "if"))
                        index += 2
                        break
                    elif kind == "ELIF" and line[index:index+4] == "elif":
                        self.tokens.append((kind, "elif"))
                        index += 4
                        break
                    elif kind == "ELSE" and line[index:index+4] == "else":
                        self.tokens.append((kind, "else"))
                        index += 4
                        break
                    elif kind == "WHILE" and line[index:index+5] == "while":
                        self.tokens.append((kind, "while"))
                        index += 5
                        break
                    elif kind == "FOR" and line[index:index+3] == "for":
                        self.tokens.append((kind, "for"))
                        index += 3
                        break
                    elif kind == "IN" and line[index:index+2] == "in":
                        self.tokens.append((kind, "in"))
                        index += 2
                        break
                    elif kind == "DEF" and line[index:index+3] == "def":
                        self.tokens.append((kind, "def"))
                        index += 3
                        break
                else:
                    raise SyntaxError(f"Unexpected character: {char}")

            self.tokens.append(("NEWLINE", "\n"))

        while len(self.indent_stack) > 1:
            self.tokens.append(("DEDENT", self.indent_stack.pop()))

    def next_token(self):
        return self.tokens.pop(0) if self.tokens else ("EOF", "EOF")

# Example Usage:
# code = """
# x = 10
# def print():
#     return 20
# """
# lexer = Lexer(code)
# print(lexer.tokens)
