class InfixToRPNConverter:
    def __init__(self):
        self.output = []
        self.operators = []
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        self.associativity = {'+': 'L', '-': 'L', '*': 'L', '/': 'L', '^': 'R'}

    def is_operator(self, token):
        return token in self.precedence

    def is_left_associative(self, token):
        return self.associativity[token] == 'L'

    def get_precedence(self, token):
        return self.precedence[token]

    def convert(self, expression):
        tokens = expression.split()
        for token in tokens:
            if token.isnumeric():  # If the token is an operand (number), add it to the output list
                self.output.append(token)
            elif self.is_operator(token):  # If the token is an operator, process it
                while (self.operators and self.operators[-1] != '(' and
                       ((self.is_left_associative(token) and self.get_precedence(token) <= self.get_precedence(self.operators[-1])) or
                        (not self.is_left_associative(token) and self.get_precedence(token) < self.get_precedence(self.operators[-1])))):
                    self.output.append(self.operators.pop())
                self.operators.append(token)
            elif token == '(':  # If the token is a left parenthesis, push it onto the stack
                self.operators.append(token)
            elif token == ')':  # If the token is a right parenthesis, pop from the stack to the output list until a left parenthesis is encountered
                while self.operators and self.operators[-1] != '(':
                    self.output.append(self.operators.pop())
                self.operators.pop()  # Discard the left parenthesis

        # Pop all the operators left in the stack
        while self.operators:
            self.output.append(self.operators.pop())

        return ' '.join(self.output)

# Example usage:
converter = InfixToRPNConverter()
infix_expression = "3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3"
rpn = converter.convert(infix_expression)
print(f"Infix: {infix_expression}")
print(f"RPN: {rpn}")





class RPNCalculator:
    def __init__(self):
        self.stack = []

    def evaluate(self, expression):
        tokens = expression.split()
        for token in tokens:
            if token.isnumeric():  # If the token is an operand (number), push it to the stack
                self.stack.append(int(token))
            else:  # If the token is an operator, pop the top two elements from the stack, apply the operator, and push the result back
                operand2 = self.stack.pop()
                operand1 = self.stack.pop()
                result = self.apply_operator(token, operand1, operand2)
                self.stack.append(result)
        return self.stack[0]  # The result will be the only element left in the stack

    def apply_operator(self, operator, operand1, operand2):
        if operator == '+':
            return operand1 + operand2
        elif operator == '-':
            return operand1 - operand2
        elif operator == '*':
            return operand1 * operand2
        elif operator == '/':
            return operand1 / operand2
        elif operator == '^':
            return operand1 ** operand2
        else:
            raise ValueError(f"Unknown operator: {operator}")
        
rpn_expression = "3 4 2 * 1 5 - 2 3 ^ ^ / +"
calculator = RPNCalculator()
result = calculator.evaluate(rpn_expression)
print(f"RPN Expression: {rpn_expression}")
print(f"Result: {result}")


converter = InfixToRPNConverter()
calculator = RPNCalculator()

infix_expression = "3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3"
rpn_expression = converter.convert(infix_expression)
result = calculator.evaluate(rpn_expression)

print(f"Infix: {infix_expression}")
print(f"RPN: {rpn_expression}")
print(f"Result: {result}")
