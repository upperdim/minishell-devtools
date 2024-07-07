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


def create_token(type: TokenType, val: str, prev: Token, next: Token):
	new = Token(type, val, prev, next)
	return new


def print_list(head: Token):
	if head is None:
		print('<null node>')
	iter = head
	while iter is not None:
		print(f'{iter.type}: {iter.val}')
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
	# TODO: handle nested single & double quotes
	return True  # TODO: placeholder, implement the function


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

	head = None
	i = 0
	curr_token_val = ''
	while i < len(line):
		# These checks shall be true only if it's the first char of a token
		if line[i] == ' ':
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
			quote_type = ("'" if line[i + 1] == "'" else '"')
			next_quote_idx = get_idx_of_next(line, i + 1, quote_type)
			curr_token_val += line[i + 1:next_quote_idx]
			i += next_quote_idx - i + 1
			i += 1
			continue
		# if one of above conditions are true, below shouldn't run

		curr_token_val += line[i]

		# These will be true on rest of the chars of the token
		if i + 1 == len(line) or line[i + 1] == ' ' or line[i + 1] == '|':
			# TODO: add current char to curr_token_val too before creating STRING type?
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
					i += 2
					continue
				else:
					# > or < w/ number
					new_val = curr_token_val + redirection_type
					new_type = (TokenType.REDIR_FROM if redirection_type == '<' else TokenType.REDIR_TO)
					head = add_token(head, Token(new_type, new_val, None, None))
					curr_token_val = ''
					i += 1
		elif line[i + 1] == "'" or line[i + 1] == '"':
			quote_type = ("'" if line[i + 1] == "'" else '"')
			# TODO: add curr char to curr_token_val before doing this?
			# append a substr of entire quote to the curr_token_val (exclude quote chars)
			next_quote_idx = get_idx_of_next(line, i + 1, quote_type)
			curr_token_val += line[i + 2:next_quote_idx]
			# increase i to be right after the quote end
			i += next_quote_idx - i + 1
		i += 1
	return head


def tests():
	def ll_to_list(head):
		result = []
		iter = head
		while iter is not None:
			result.append(iter)
		return result

	# TODO: remove cases with invalid quotes
	# TODO: convert str lists to Token object lists in expected cases
	# TODO: use ll_to_list() to convert actual ll into list and compare with expecteds
	tests = [
		# Split from redirecitons
		#['echo asd>hello', ['echo', 'asd', '>', 'hello']],
		#['echo asd<hello', ['echo', 'asd', '<', 'hello']],
		['echo asd>>hello', ['echo', 'asd', '>>', 'hello']],
		['echo asd<<hello', ['echo', 'asd', '<<', 'hello']],

		# Quote Adjacent Redirections
		# Exception: Redirections near quotes create their own words
		#
		# IDEA 1: make an exception list of patterns that will be ignored by the rule that separates this quote
		# IDEA 2: just do another pass looking for redirection patterns and quotes. Can be done even in token linked list
		#['cat <<" EOF"', ['cat', '<<', ' EOF']],
		['cat <" EOF"', ['cat', '<', ' EOF']],
		['cat >>" EOF"', ['cat', '>>', ' EOF']],
		['cat >" EOF"', ['cat', '>', ' EOF']],
		['cat <<\' EOF\'', ['cat', '<<', ' EOF']],
		['cat <\' EOF\'', ['cat', '<', ' EOF']],
		['cat >>\' EOF\'', ['cat', '>>', ' EOF']],
		['cat >\' EOF\'', ['cat', '>', ' EOF']],
		
		# Redirections w/ prefix & fd
		['cat hello<<" EOF"', ['cat', 'hello', '<<', ' EOF']],
		['cat 123<<" EOF"', ['cat', '123<<', ' EOF']],
		['cat hello123<<" EOF"', ['cat', 'hello123', '<<', ' EOF']], # has to be entirely digits like above in order to get detected as a file descriptor for the redirection
		['cat hello1>file2name 123>file1name123>world<<" EOF"', ['cat', 'hello1', '>', 'file2name', '123>', 'file1name123', '>', 'world', '<<', ' EOF']],

		# Redirections w/ prefix & fd: RANGE CHECK
		['cat -12> filename', ['cat', '-12', '>', 'filename']], # since - is not digit, negative numbers count as filenames
		['cat 2147483647> filename', ['cat', '2147483647>', 'filename']],
		['cat 2147483648> filename', ['cat', '2147483648', '>', 'filename']],

		# Error handling for invalid inputs
		#
		# These will be labeled as SYNTAX ERRORs either after tokenization or maybe here in lexing process
		# If you have a reliable way of cutting them out, just stop processing and give error to user
		['cat << >> <" EOF"', ['cat', '<<', '>>', '<', ' EOF']], # expected is discussible
		['cat <<>> <" EOF"', ['cat', '<<', '>>', '<', ' EOF']],  # expected is discussible

		# Expansion
		# TBA
		
		# Quotes & Spaces
		['export VAR="echo hi | cat"', ['export', 'VAR=echo hi | cat']],
		['echo "Hello"World', ['echo', 'HelloWorld']],
		['echo Hello World', ['echo', 'Hello', 'World']],
		['echo "Hello  World"', ['echo', 'Hello  World']],
		['echo "Hello\' World"', ['echo', "Hello' World"]],
		['echo "Hello" World"', ['echo', 'Hello', 'World"']],
		['echo Hello" World', ['echo', 'Hello"', 'World']],
		['echo Hello"World"       ', ['echo', 'HelloWorld']],
		['echo              Hello"World"\'stuck\'        ', ['echo', 'HelloWorldstuck']],
		['ec ho"  \'Hello  "World\'  x ', ['ec', "ho  'Hello  World'", 'x']],
		['"\'"\'\'"\'"', ["''"]],
		['a"\'123\'456"', ["a'123'456"]],
		['"\'123\'456"', ["'123'456"]],
		['"\'"', ["'"]],
		["''", ['']],
		['""', ['']],
		['\'"\'', ['"']],
		['\'\'"\'"', ["'"]],
		['echo" Hello World"', ['echo Hello World']],
		['"no clue of \'\'what other test   "to do\'', ["no clue of ''what other test   to", "do'"]],

		# Pipes
		['echo hi | cat -e', ['echo', 'hi', '|', 'cat', '-e']],
		['echo hi|cat"asd" -e', ['echo', 'hi', '|', 'catasd', '-e']],
		['echo hi|cat -e', ['echo', 'hi', '|', 'cat', '-e']],
		['echo "hi|cat" -e', ['echo', 'hi|cat', '-e']],
		['echo hi"|"cat -e', ['echo', 'hi|cat', '-e']],
	]


def ll_test_1():
	print(f'Runnig test #1:')
	n3 = Token(TokenType.STRING, "!", None, None)
	n2 = Token(TokenType.STRING, "world", n3, None)
	n1 = Token(TokenType.STRING, "hello", n2, None)
	n2.prev = n1
	print_list(n1)
	print_list(n1)

def ll_test_2():
	print(f'Runnig test #2:')
	head = None
	print_list(head)
	head = add_token(head, Token(TokenType.STRING, "one", None, None))
	print_list(head)
	head = add_token(head, Token(TokenType.STRING, "two", None, None))
	print_list(head)
	head = add_token(head, Token(TokenType.STRING, "three", None, None))
	print_list(head)


def interactive():
	while True:
		line = input('$ ')
		if not validate_quotes(line):
			print('Invalid input: unclosed quotes')
		else:
			tokens = parse(line)
			print_list(tokens)


def main():
	# ll_test_1()
	# ll_test_2()
	# interactive()
	tests()


if __name__ == '__main__':
	main()
