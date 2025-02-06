class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.index = 0
        self.advance()

    def advance(self):
        """Move to the next token."""
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
            self.index += 1
        else:
            self.current_token = ("EOF", "")

    def peek(self, n):
        """Look ahead n tokens."""
        if self.index + n - 1 < len(self.tokens):
            return self.tokens[self.index + n - 1]
        return ("EOF", "")

    def eat(self, token_type):
        """Consume the current token if it matches the token_type."""
        if self.current_token[0] == token_type:
            self.advance()
        else:
            raise SyntaxError(f"Expected {token_type}, got {self.current_token}")

    def program(self):
        """Parse the entire program."""
        statements = []
        while self.current_token[0] not in ["EOF"]:
            statements.extend(self.statement())
        return statements

    def statement(self):
        statements = []
        while self.current_token[0] not in ["NEWLINE", "DEDENT", "EOF"]:
            print(f"Current token in statement: {self.current_token}")  # Debugging line

            # Handle assignment (IDENTIFIER followed by '=')
            if self.current_token[0] == "IDENTIFIER":
                # Check if it's an assignment or function call or function definition
                if self.peek(1)[0] == "ASSIGN":  # Check if the next token is '=' for assignment
                    statements.append(self.assignment())
                elif self.peek(1)[0] == "LPAREN":  # Check if the next token is '(' for function call
                    statements.append(self.function_call())  # Handle function call
                else:
                    raise SyntaxError(f"Unexpected token after IDENTIFIER: {self.peek(1)}")

            # Handle other statements
            elif self.current_token[0] == "IF":
                statements.append(self.if_stmt())
            elif self.current_token[0] == "FOR":
                statements.append(self.for_stmt())
            elif self.current_token[0] == "WHILE":
                statements.append(self.while_stmt())
            elif self.current_token[0] == "DEF":
                statements.append(self.function_def())  # Function definition parsing here
            elif self.current_token[0] == "RETURN":
                statements.append(self.return_stmt())  # Handle return statements
            else:
                raise SyntaxError(f"Unexpected token: {self.current_token}")

            # Consume the current token
            self.eat(self.current_token[0])

            if self.current_token[0] == "SEMICOLON":  # Handle multiple statements on the same line
                self.eat("SEMICOLON")
            else:
                break  # Stop if no semicolon or end of line

        return statements

    def assignment(self):
        """Parse an assignment statement."""
        var_name = self.current_token[1]
        self.eat("IDENTIFIER")  # Consume identifier token
        self.eat("ASSIGN")  # Consume '='
        expr = self.expression()
        return ("ASSIGN", var_name, expr)

    def return_stmt(self):
        """Parse a return statement."""
        self.eat("RETURN")  # Consume 'return'
        value = self.expression()  # Parse the return value expression
        return ("RETURN", value)

    def if_stmt(self):
        """Parse an if statement."""
        self.eat("IF")  # Consume 'if'
        condition = self.expression()
        self.eat("COLON")  # Consume ':'
        true_branch = self.block()
        false_branch = None

        if self.current_token[0] == "ELIF":
            self.eat("ELIF")
            false_branch = self.if_stmt()

        elif self.current_token[0] == "ELSE":
            self.eat("ELSE")
            false_branch = self.block()

        return ("IF", condition, true_branch, false_branch)

    def for_stmt(self):
        """Parse a for loop statement."""
        self.eat("FOR")  # Consume 'for'
        var_name = self.current_token[1]
        self.eat("IDENTIFIER")  # Consume identifier token
        self.eat("IN")  # Consume 'in'
        start = self.expression()
        self.eat("TO")  # Consume 'to'
        end = self.expression()
        self.eat("COLON")  # Consume ':'
        body = self.block()
        return ("FOR", var_name, start, end, body)

    def while_stmt(self):
        """Parse a while loop statement."""
        self.eat("WHILE")  # Consume 'while'
        condition = self.expression()
        self.eat("COLON")  # Consume ':'
        body = self.block()
        return ("WHILE", condition, body)

    def function_def(self):
        """Parse a function definition."""
        self.eat("DEF")  # Consume 'def'
        func_name = self.current_token[1]
        self.eat("IDENTIFIER")  # Consume function name
        self.eat("LPAREN")  # Consume '('
        params = self.parameters()
        self.eat("RPAREN")  # Consume ')'
        self.eat("COLON")  # Consume ':'

        # After the colon, we expect an indented block (function body)
        self.eat("NEWLINE")  # Consume newline after function declaration
        body = self.block()  # Parse the function's body (block of statements)

        return ("DEF", func_name, params, body)

    def parameters(self):
        """Parse function parameters."""
        params = []
        if self.current_token[0] != "RPAREN":
            while self.current_token[0] == "IDENTIFIER":
                params.append(self.current_token[1])
                self.eat("IDENTIFIER")
                if self.current_token[0] == "COMMA":
                    self.eat("COMMA")
        return params

    def block(self):
        """Parse a block of statements (for if, for, while, or function)."""
        self.eat("INDENT")  # Consume indentation token
        statements = []
        while self.current_token[0] not in ["DEDENT", "EOF"]:
            statements.extend(self.statement())
        self.eat("DEDENT")  # Consume dedentation
        return statements

    def function_call(self):
        """Parse a function call."""
        func_name = self.current_token[1]  # The function name is the identifier
        self.eat("IDENTIFIER")  # Consume the identifier token
        self.eat("LPAREN")  # Consume '('
        args = self.arguments()  # Parse the function arguments
        self.eat("RPAREN")  # Consume ')'
        return ("CALL", func_name, args)

    def arguments(self):
        """Parse the arguments for a function call."""
        args = []
        if self.current_token[0] != "RPAREN":
            while True:
                args.append(self.expression())  # Parse an argument
                if self.current_token[0] == "COMMA":
                    self.eat("COMMA")  # Consume the comma
                else:
                    break
        return args

    def expression(self):
        """Parse an expression.""" 
        return self.term()

    def term(self):
        """Parse a term (currently only factors)."""
        return self.factor()

    def factor(self):
        """Parse a factor, like numbers or identifiers."""
        if self.current_token[0] == "NUMBER":
            value = self.current_token[1]
            self.eat("NUMBER")
            return ("NUM", value)
        elif self.current_token[0] == "IDENTIFIER":
            value = self.current_token[1]
            self.eat("IDENTIFIER")
            return ("VAR", value)
        elif self.current_token[0] == "LPAREN":
            self.eat("LPAREN")
            expr = self.expression()
            self.eat("RPAREN")
            return expr
        else:
            raise SyntaxError(f"Unexpected token {self.current_token}")

