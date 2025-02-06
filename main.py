#! /usr/bin/python3
import sys
from lexer import Lexer
from parser import Parser

def main():
    code_file = sys.argv[1]
    with open(code_file, "r") as file:
        code = file.read()

    lexer = Lexer(code)
    print("Tokens:",lexer.tokens)
    parser = Parser(lexer.tokens)
    try:
        AST = parser.program()
        print("Abstract Syntax Tree:")
        print(AST)
    except SyntaxError as e:
        print(f"Syntax Error: {e}")

main()
