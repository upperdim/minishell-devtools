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


def tokenize(line):
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

	def handle_if_first_char(line, i, curr_token_val, head):
		'''These checks shall be true only if it's the first char of a token'''
		if line[i] == ' ':
			if len(curr_token_val) > 0:
				head = add_token(head, Token(TokenType.STRING, curr_token_val, None, None))
				curr_token_val = ''
			return True, line, i, curr_token_val, head
		elif line[i] == '|':
			head = add_token(head, Token(TokenType.PIPE, "|", None, None))
			return True, line, i, curr_token_val, head
		elif line[i] == '<':
			if i != len(line) and line[i + 1] != '<':
				head = add_token(head, Token(TokenType.REDIR_FROM, '<', None, None))
			else:
				head = add_token(head, Token(TokenType.HERE_DOC, '<<', None, None))
				i += 1
			return True, line, i, curr_token_val, head
		elif line[i] == '>':
			if i != len(line) and line[i + 1] != '>':
				head = add_token(head, Token(TokenType.REDIR_TO, '>', None, None))
			else:
				head = add_token(head, Token(TokenType.APPEND_TO, '>>', None, None))
				i += 1
			return True, line, i, curr_token_val, head
		elif line[i] == "'" or line[i] == '"':
			curr_token_val, i, head = handle_quotes(line, i, 0, curr_token_val, head)
			return True, line, i, curr_token_val, head
		return False, line, i, curr_token_val, head

	head = None
	i = 0
	curr_token_val = ''
	while i < len(line):
		is_first_char, line, i, curr_token_val, head = handle_if_first_char(line, i, curr_token_val, head)
		if is_first_char:
			i += 1
			continue

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
					i += 2
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
