# Reverse Polish Notation
#
# Converts infix mathematical expressions to Reverse Polish Notation, parses and solves them.

from enum import Enum


class RPN:
	class TokenType(Enum):
		OPERATOR = 1
		NUMBER = 2
		SPACE = 3

	class Token:
		def __init__(self, type, value):
			self.type = type
			self.value = value

	_op_presedences = {"(": 0, "^": 5, "/": 4, "*": 3, "+": 2, "-": 1}
	_lex_cursor_pos = 0

	def _do_operation(operand1, operator, operand2):
		operand1 = operand1.value
		operand2 = operand2.value
		operator = operator.value
		if operator == '^':
			return RPN.Token(RPN.TokenType.NUMBER, operand1**operand2)
		elif operator == '/':
			return RPN.Token(RPN.TokenType.NUMBER, operand1 // operand2)
		elif operator == '*':
			return RPN.Token(RPN.TokenType.NUMBER, operand1 * operand2)
		elif operator == '+':
			return RPN.Token(RPN.TokenType.NUMBER, operand1 + operand2)
		elif operator == '-':
			return RPN.Token(RPN.TokenType.NUMBER, operand1 - operand2)
		else:
			raise Exception('do_operation(): Invalid operator.')

	def _lex(expr):
			"""return the next token from expression, return None if no tokens left"""
			if RPN._lex_cursor_pos >= len(expr):
				return None
			elif expr[RPN._lex_cursor_pos] in "()^/*+-":
				result = RPN.Token(RPN.TokenType.OPERATOR, expr[RPN._lex_cursor_pos])
				RPN._lex_cursor_pos += 1
				return result
			elif expr[RPN._lex_cursor_pos].isdigit():
				value = 0
				while RPN._lex_cursor_pos < len(expr) and expr[RPN._lex_cursor_pos].isdigit():
					value *= 10
					value += int(expr[RPN._lex_cursor_pos])
					RPN._lex_cursor_pos += 1
				return RPN.Token(RPN.TokenType.NUMBER, value)
			elif expr[RPN._lex_cursor_pos] == ' ':
				RPN._lex_cursor_pos += 1
				return RPN.Token(RPN.TokenType.SPACE, ' ')
			else:
				raise Exception("lex(): Invalid character in expr")

	def _convert_to_rpn_tokens(infix_expr):
		"""create a stack of tokens in reverse polish notation form"""
		output_stack = []
		holding_stack = []
		RPN._lex_cursor_pos = 0
		token = RPN._lex(infix_expr)
		while token is not None:
			if token.type == RPN.TokenType.NUMBER:
				output_stack.append(token)
			elif token.type == RPN.TokenType.OPERATOR:
				if token.value == '(':
					holding_stack.append(token)
				elif token.value == ')':
					# Pop holding stack and push into output stack until you reach opening paranthesis
					elem = holding_stack.pop()
					while elem.value != '(':
						output_stack.append(elem)
						elem = holding_stack.pop()
				else:
					while len(holding_stack) > 0 and RPN._op_presedences[token.value] < RPN._op_presedences[holding_stack[-1].value]:
						output_stack.append(holding_stack.pop())
					holding_stack.append(token)
			elif token.type == RPN.TokenType.SPACE:
				pass
			token = RPN._lex(infix_expr)
		while len(holding_stack) > 0:
			output_stack.append(holding_stack.pop())
		return output_stack
	
	def convert(infix_expr):
		"""convert infix expression into reverse polish notation"""
		rpn_tokens = RPN._convert_to_rpn_tokens(infix_expr)
		result = ""
		for token in rpn_tokens:
			result += str(token.value)
			result += ' '
		return result

	def _solve_from_rpn_tokens(rpn_tokens):
		solve_stack = []
		while len(rpn_tokens) > 0:
			elem = rpn_tokens.pop(0)
			if elem.type == RPN.TokenType.NUMBER:
				solve_stack.append(elem)
			elif elem.type == RPN.TokenType.OPERATOR:
				operand2 = solve_stack.pop()
				operand1 = solve_stack.pop()
				solve_stack.append(RPN._do_operation(operand1, elem, operand2))
		return solve_stack[0].value

	def solve_infix(infix_expr):
		"""solve an infix expression"""
		rpn_tokens = RPN._convert_to_rpn_tokens(infix_expr)
		return RPN._solve_from_rpn_tokens(rpn_tokens)

	def _tokenize_rpn(rpn_expr):
		tokens = []
		RPN._lex_cursor_pos = 0
		token = RPN._lex(rpn_expr)
		while token is not None:
			tokens.append(token)
			token = RPN._lex(rpn_expr)
		return tokens

	def solve_rpn(rpn_expr):
		"""solve a reverse polish notation expression"""
		rpn_tokens = RPN._tokenize_rpn(rpn_expr)
		return RPN._solve_from_rpn_tokens(rpn_tokens)


def	main():
	infix_expressions = [
		"10 + 2 * 4 - 3",
		"1 + 2 * ( 4 - 3 )",
		"( 1 + 2 ) * 4 - 3",
		"1 + 2 * ( 2 ^ ( 2 + 1 ) - 5 )",
		"1 + 2 * ( 2 ^ 2 ^ 2 - 5 )",
	]

	for infix_expr in infix_expressions:
		print(f'Infix expression        = {infix_expr}')
		print(f'Reverse Polish Notation = {RPN.convert(infix_expr)}')
		print(f'Solution                = {RPN.solve_infix(infix_expr)}\n')

	rpn_expressions = [
		"8 9 * 9 - 9 - 9 - 4 - 1 +",
		"7 7 * 7 -",
		"1 2 * 2 / 2 * 2 4 - +",
		"10 2 4 * + 3 -"
	]

	for rpn_expr in rpn_expressions:
		print(f'Reverse Polish Notation = {rpn_expr}')
		print(f'Solution                = {RPN.solve_rpn(rpn_expr)}\n')

if __name__ == '__main__':
	main()
