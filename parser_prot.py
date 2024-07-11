from dataclasses import dataclass
from enum import Enum
from typing import TypeVar


class TokenType(Enum):
	UNKNOWN = 0
	STRING = 1
	REDIR_TO = 2
	APPEND_TO = 3
	REDIR_FROM = 4
	HERE_DOC = 5
	PIPE = 6


Token = TypeVar("Token")
INT_MAX = 2147483647


@dataclass
class Token:
	type: TokenType
	val: str
	next: Token
	prev: Token


def print_ll(head: Token, lines_prefix: str=''):
	if head is None:
		print(f'{lines_prefix}<null node>')
	iter = head
	while iter is not None:
		print(f'{lines_prefix}{iter.type}: ({iter.val})')
		iter = iter.next


def add_token(head: Token, new: Token):
	if head is None:
		head = new
		return head
	iter = head
	while iter.next is not None:
		iter = iter.next
	iter.next = new
	new.prev = iter
	return head


def validate_quotes(line):
	'''Checks whether single and double quotes were closed correctly or not'''
	quote_type = None
	for c in line:
		if quote_type is None and (c == '"' or c == "'"):
			quote_type = c
		elif quote_type == c:
			quote_type = None
	return quote_type is None


def parse(line):
	def get_idx_of_next(s, search_start_idx, search_char):
		'''
		Search `search_char` in `s` starting from index `search_start_idx`.
		Return -1 if not found
		'''
		i = search_start_idx
		while i < len(s):
			if s[i] == search_char:
				return i
			i += 1
		return -1
	
	def handle_quotes(line, i, idx_dist_to_quote, curr_token_val, head):
		'''
		Updates `quote_token_val` and adjusts `i` after properly handling quotes.

		Inputs:
		- line              : input line
		- i                 : current index in the line
		- idx_dist_to_quote : adding this to `i` should give index of the opening quote

		Outputs:
		- curr_token_val : updated current token value
		- i              : updated index position in the line  
		'''
		quote_type = ("'" if line[i + idx_dist_to_quote] == "'" else '"')
		# append a substr of entire quote to the curr_token_val (exclude quote chars)
		next_quote_idx = get_idx_of_next(line, i + idx_dist_to_quote + 1, quote_type)
		if next_quote_idx == -1:
			# next quote not found, just append the quote char itself
			# curr_token_val += line[i + idx_dist_to_quote:i + idx_dist_to_quote + 1]
			# i += 1

			# or instead of dealing with edge cases and bugs of this, just say invalid syntax and quit
			print('SyntaxError: unclosed quotes')
			exit()
		elif next_quote_idx == i + idx_dist_to_quote + 1:
			if len(curr_token_val) == 0:
				head = add_token(head, Token(TokenType.STRING, '', None, None))
			i += 1
		else:
			curr_token_val += line[i + idx_dist_to_quote + 1:next_quote_idx]
			i += next_quote_idx - i
		return curr_token_val, i, head

	if not validate_quotes(line):
		print('SyntaxError: unclosed quotes')
		return
	head = None
	i = 0
	curr_token_val = ''
	while i < len(line):
		# These checks shall be true only if it's the first char of a token
		if line[i] == ' ':
			if len(curr_token_val) > 0:
				head = add_token(head, Token(TokenType.STRING, curr_token_val, None, None))
				curr_token_val = ''
			i += 1
			continue
		elif line[i] == '|':
			head = add_token(head, Token(TokenType.PIPE, "|", None, None))
			i += 1
			continue
		elif line[i] == '<':
			if i != len(line) and line[i + 1] != '<':
				head = add_token(head, Token(TokenType.REDIR_FROM, '<', None, None))
				i += 1
				continue
			else:
				head = add_token(head, Token(TokenType.HERE_DOC, '<<', None, None))
				i += 2
				continue
		elif line[i] == '>':
			if i != len(line) and line[i + 1] != '>':
				head = add_token(head, Token(TokenType.REDIR_TO, '>', None, None))
				i += 1
				continue
			else:
				head = add_token(head, Token(TokenType.APPEND_TO, '>>', None, None))
				i += 2
				continue
		elif line[i] == "'" or line[i] == '"':
			curr_token_val, i, head = handle_quotes(line, i, 0, curr_token_val, head)
			i += 1
			continue
		# if one of above conditions are true, below shouldn't run

		curr_token_val += line[i]

		# These will be true on rest of the chars of the token
		if i + 1 == len(line) or line[i + 1] == ' ' or line[i + 1] == '|':
			head = add_token(head, Token(TokenType.STRING, curr_token_val, None, None))
			curr_token_val = ''
		elif line[i + 1] == '>' or line[i + 1] == '<':
			redirection_type = ('>' if line[i + 1] == '>' else '<')
			if not curr_token_val.isnumeric():
				head = add_token(head, Token(TokenType.STRING, curr_token_val, None, None))
				curr_token_val = ''
			else:
				curr_token_num = int(curr_token_val)
				if curr_token_num > INT_MAX or curr_token_num < 0:
					head = add_token(head, Token(TokenType.STRING, curr_token_val, None, None))
					curr_token_val = ''
				elif i + 2 < len(line) and (line[i + 2] == redirection_type):
					# >> or << w/ number
					new_val = curr_token_val + redirection_type + redirection_type
					new_type = (TokenType.HERE_DOC if redirection_type == '<' else TokenType.APPEND_TO)
					head = add_token(head, Token(new_type, new_val, None, None))
					curr_token_val = ''
					i += 3
					continue
				else:
					# > or < w/ number
					new_val = curr_token_val + redirection_type
					new_type = (TokenType.REDIR_FROM if redirection_type == '<' else TokenType.REDIR_TO)
					head = add_token(head, Token(new_type, new_val, None, None))
					curr_token_val = ''
					i += 1
		elif line[i + 1] == "'" or line[i + 1] == '"':
			curr_token_val, i, head = handle_quotes(line, i, 1, curr_token_val, head)
		i += 1
	if len(curr_token_val) > 0:
		head = add_token(head, Token(TokenType.STRING, curr_token_val, None, None))
	return head


def parser_tests():
	print('Running parser tests...')

	def is_ll_equal_list(head: Token, token_list):
		i = 0
		iter = head
		while iter is not None:
			if iter.val != token_list[i][0] or iter.type != token_list[i][1]:
				return -1
			iter = iter.next
			i += 1
		if i != len(token_list):
			return -2
		return 1

	tests = [
		# Currently debugging
		
		# Split from redirecitons
		['echo asd>hello', 
   			[['echo', TokenType.STRING],
	   		['asd', TokenType.STRING],
			['>', TokenType.REDIR_TO],
			['hello', TokenType.STRING]
			]
		],
		['echo asd<hello',
   			[['echo', TokenType.STRING],
	   		['asd', TokenType.STRING],
			['<', TokenType.REDIR_FROM],
			['hello', TokenType.STRING]
			]
		],
		['echo asd>>hello',
   			[['echo', TokenType.STRING],
	   		['asd', TokenType.STRING],
			['>>', TokenType.APPEND_TO],
			['hello', TokenType.STRING]
			]
		],
		['echo asd<<hello',
   			[['echo', TokenType.STRING],
	   		['asd', TokenType.STRING],
			['<<', TokenType.HERE_DOC],
			['hello', TokenType.STRING],
			]
		],

		# Quote Adjacent Redirections
		# Exception: Redirections near quotes create their own words
		#
		# IDEA 1: make an exception list of patterns that will be ignored by the rule that separates this quote
		# IDEA 2: just do another pass looking for redirection patterns and quotes. Can be done even in token linked list
		['cat <<" EOF"',
   			[['cat', TokenType.STRING],
	   		['<<', TokenType.HERE_DOC],
			[' EOF', TokenType.STRING],
			]
		],
		['cat <" EOF"',
   			[['cat', TokenType.STRING],
	   		['<', TokenType.REDIR_FROM],
			[' EOF', TokenType.STRING],
			]
		],
		['cat >>" EOF"',
   			[['cat', TokenType.STRING],
	   		['>>', TokenType.APPEND_TO],
			[' EOF', TokenType.STRING],
			]
		],
		['cat >" EOF"',
   			[['cat', TokenType.STRING],
	   		['>', TokenType.REDIR_TO],
			[' EOF', TokenType.STRING],
			]
		],
		['cat <<\' EOF\'',
   			[['cat', TokenType.STRING],
	   		['<<', TokenType.HERE_DOC],
			[' EOF', TokenType.STRING],
			]
		],
		['cat <\' EOF\'',
   			[['cat', TokenType.STRING],
	   		['<', TokenType.REDIR_FROM],
			[' EOF', TokenType.STRING],
			]
		],
		['cat >>\' EOF\'',
   			[['cat', TokenType.STRING],
	   		['>>', TokenType.APPEND_TO],
			[' EOF', TokenType.STRING],
			]
		],
		['cat >\' EOF\'',
   			[['cat', TokenType.STRING],
	   		['>', TokenType.REDIR_TO],
			[' EOF', TokenType.STRING],
			]
		],
		
		# Redirections w/ prefix & fd
		['cat hello<<" EOF"',
   			[['cat', TokenType.STRING],
	   		['hello', TokenType.STRING],
			['<<', TokenType.HERE_DOC],
			[' EOF', TokenType.STRING],
			]
		],
		['cat 123<<" EOF"',
   			[['cat', TokenType.STRING],
			['123<<', TokenType.HERE_DOC],
			[' EOF', TokenType.STRING],
			]
		],
		['cat hello123<<" EOF"',
   			[['cat', TokenType.STRING],
			['hello123', TokenType.STRING],
			['<<', TokenType.HERE_DOC],
			[' EOF', TokenType.STRING],
			]
		], # has to be entirely digits like above in order to get detected as a file descriptor for the redirection
		['cat hello1>file2name 123>file1name123>world<<" EOF"',
   			[['cat', TokenType.STRING],
			['hello1', TokenType.STRING],
			['>', TokenType.REDIR_TO],
			['file2name', TokenType.STRING],
			['123>', TokenType.REDIR_TO],
			['file1name123', TokenType.STRING],
			['>', TokenType.REDIR_TO],
			['world', TokenType.STRING],
			['<<', TokenType.HERE_DOC],
			[' EOF', TokenType.STRING],
			]
		],

		# Redirections w/ prefix & fd: RANGE CHECK
		['cat -12> filename',
   			[['cat', TokenType.STRING],
	   		['-12', TokenType.STRING],
			['>', TokenType.REDIR_TO],
			['filename', TokenType.STRING],
			]
		], # since - is not digit, negative numbers count as filenames
		['cat 2147483647> filename',
   			[['cat', TokenType.STRING],
	   		['2147483647>', TokenType.REDIR_TO],
			['filename', TokenType.STRING],
			]
		],
		['cat 2147483648> filename',
   			[['cat', TokenType.STRING],
	   		['2147483648', TokenType.STRING],
			['>', TokenType.REDIR_TO],
			['filename', TokenType.STRING],
			]
		],

		# Error handling for invalid inputs
		#
		# These will be labeled as SYNTAX ERRORs either after tokenization or maybe here in lexing process
		# If you have a reliable way of cutting them out, just stop processing and give error to user
		['cat << >> <" EOF"',
   			[['cat', TokenType.STRING],
	   		['<<', TokenType.HERE_DOC],
			['>>', TokenType.APPEND_TO],
			['<', TokenType.REDIR_FROM],
			[' EOF', TokenType.STRING],
			]
		], # expected is discussible
		['cat <<>> <" EOF"',
   			[['cat', TokenType.STRING],
	   		['<<', TokenType.HERE_DOC],
			['>>', TokenType.APPEND_TO],
			['<', TokenType.REDIR_FROM],
			[' EOF', TokenType.STRING],
			]
		],  # expected is discussible

		# Expansion
		# TBA
		
		# Quotes & Spaces
		['export VAR="echo hi | cat"',
			[['export', TokenType.STRING],
			['VAR=echo hi | cat', TokenType.STRING],
			]
		],
		['echo "Hello"World',
   			[['echo', TokenType.STRING],
			['HelloWorld', TokenType.STRING],
			]
		],
		['echo Hello World',
   			[['echo', TokenType.STRING],
	   		['Hello', TokenType.STRING],
			['World', TokenType.STRING],
			]
		],
		['echo "Hello  World"',
   			[['echo', TokenType.STRING],
	   		['Hello  World', TokenType.STRING],
			]
		],
		['cat "hello" x',
			[['cat', TokenType.STRING],
			['hello', TokenType.STRING],
			['x', TokenType.STRING],
			]
		],
		['echo Hello"World"       ',
   			[['echo', TokenType.STRING],
	   		['HelloWorld', TokenType.STRING],
			]
		],
		['echo              Hello"World"\'stuck\'        ',
   			[['echo', TokenType.STRING],
	   		['HelloWorldstuck', TokenType.STRING],
			]
		],
		['"\'"\'\'"\'"',
			[["''", TokenType.STRING]]
		],
		['a"\'123\'456"',
   			[["a'123'456", TokenType.STRING]]
		],
		['"\'123\'456"',
   			[["'123'456", TokenType.STRING]]
		],
		['"\'"',
   			[["'", TokenType.STRING]]
		],
		["''",
   			[['', TokenType.STRING]]
		],
		['""',
   			[['', TokenType.STRING]]
		],
		['\'"\'',
   			[['"', TokenType.STRING]]
		],
		['\'\'"\'"',
   			[["", TokenType.STRING],
	   		["'", TokenType.STRING]
			]
		],
		['echo" Hello World"',
   			[["echo Hello World", TokenType.STRING]]
		],
		['"no clue of \'\'what other test   "to do',
   			[["no clue of ''what other test   to", TokenType.STRING],
	   		["do", TokenType.STRING],
			]
		],
		['" dog" cat',
   			[[" dog", TokenType.STRING],
	   		["cat", TokenType.STRING],
			]
		],
		['echo asd << "" << file2',
			[['echo', TokenType.STRING],
			['asd', TokenType.STRING],
			['<<', TokenType.HERE_DOC],
			['', TokenType.STRING],
			['<<', TokenType.HERE_DOC],
			['file2', TokenType.STRING],
			]
		],

		# Pipes
		['echo hi | cat -e',
   			[["echo", TokenType.STRING],
	   		["hi", TokenType.STRING],
			["|", TokenType.PIPE],
			["cat", TokenType.STRING],
			["-e", TokenType.STRING],
			]
		],
		['echo hi|cat -e',
   			[["echo", TokenType.STRING],
	   		["hi", TokenType.STRING],
			["|", TokenType.PIPE],
			["cat", TokenType.STRING],
			["-e", TokenType.STRING],
			]
		],
		['echo hi|cat"asd" -e',
   			[["echo", TokenType.STRING],
	   		["hi", TokenType.STRING],
			["|", TokenType.PIPE],
			["catasd", TokenType.STRING],
			["-e", TokenType.STRING],
			]
		],
		['echo "hi|cat" -e',
   			[["echo", TokenType.STRING],
	   		["hi|cat", TokenType.STRING],
			["-e", TokenType.STRING],
			]
		],
		['echo hi"|"cat -e',
   			[["echo", TokenType.STRING],
	   		["hi|cat", TokenType.STRING],
			["-e", TokenType.STRING],
			]
		],

		# Unclosed Quotes
		# ['ec ho"  \'Hello  "World\'  x ',
		# 	[['ec', TokenType.STRING],
		# 	["ho  'Hello  World'", TokenType.STRING],
		# 	['x', TokenType.STRING],
		# 	]
		# ],
		# ['echo >>"hi"\'x y ',
   		# 	[['echo', TokenType.STRING],
	   	# 	['>>', TokenType.APPEND_TO],
	   	# 	["hi'x", TokenType.STRING],
		# 	['y', TokenType.STRING],
		# 	]
		# ],
		# ['echo >>"hi"\'',
   		# 	[['echo', TokenType.STRING],
	   	# 	['>>', TokenType.APPEND_TO],
	   	# 	["hi'", TokenType.STRING],
		# 	]
		# ],
		# ['echo "Hello\' World"',
   		# 	[["echo", TokenType.STRING],
	  	# 	["Hello' World", TokenType.STRING],
		# 	]
		# ],
		# ['echo "Hello" World"',
   		# 	[["echo", TokenType.STRING],
	   	# 	['Hello', TokenType.STRING],
	   	# 	['World"', TokenType.STRING],
		# 	]
		# ],
		# ['echo Hello" World',
   		# 	[["echo", TokenType.STRING],
	   	# 	['Hello"', TokenType.STRING],
	   	# 	['World', TokenType.STRING],
		# 	]
		# ],
	]
	
	failed_count = 0
	for i, test in enumerate(tests):
		# print(f'i={i} test case = {test[0]}')
		actual_ll_head = parse(test[0])
		expected_list = test[1]
		is_equal = is_ll_equal_list(actual_ll_head, expected_list)
		if is_equal != 1:
			failed_count += 1
			print(f'\nFailed test {i + 1}')
			print(f'Test case = {test[0]}')
			print(f'Actual    = ')
			print_ll(actual_ll_head, '\t')
			print(f'Expected  = {expected_list}')
			if is_equal == -2:
				print(f'MISMATCHING TOKEN LIST SIZES')
	if failed_count == 0:
		print(f'OK')
	else:
		print(f'\nFailed {failed_count} tests.')


def ll_test_1():
	print(f'Runnig test #1:')
	n3 = Token(TokenType.STRING, "!", None, None)
	n2 = Token(TokenType.STRING, "world", n3, None)
	n1 = Token(TokenType.STRING, "hello", n2, None)
	n2.prev = n1
	print_ll(n1)
	print_ll(n1)

def ll_test_2():
	print(f'Runnig test #2:')
	head = None
	print_ll(head)
	head = add_token(head, Token(TokenType.STRING, "one", None, None))
	print_ll(head)
	head = add_token(head, Token(TokenType.STRING, "two", None, None))
	print_ll(head)
	head = add_token(head, Token(TokenType.STRING, "three", None, None))
	print_ll(head)


def quote_validation_tests():
	print('Running quote validation tests...')

	quote_val_tests = [
		['', True],
		['\'', False],
		['\"', False],
		['\'\'', True],
		['""', True],
		['\'\'\'', False],
		['"""', False],
		[' " \' " ', True],
		[' " \' " \' " ', False],
	]

	failed_count = 0
	for i, test in enumerate(quote_val_tests):
		# print(f'i={i} test case = {test[0]}')
		actual = validate_quotes(test[0])
		expected = test[1]
		if actual != expected:
			failed_count += 1
			print(f'\nFailed test {i + 1}')
			print(f'Test case = {test[0]}')
			print(f'Actual    = {actual}')
			print(f'Expected  = {expected}')
	if failed_count == 0:
		print(f'OK')
	else:
		print(f'\nFailed {failed_count} tests.')

	
def interactive():
	while True:
		line = input('$ ')
		if not validate_quotes(line):
			print('Invalid input: unclosed quotes')
		else:
			tokens = parse(line)
			print_ll(tokens)


def main():
	# ll_test_1()
	# ll_test_2()
	# interactive()
	quote_validation_tests()
	parser_tests()


if __name__ == '__main__':
	main()
