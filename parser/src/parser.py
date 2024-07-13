from expansion import detect_expansions, expand
from tokenizer import tokenize
from tokenizer import TokenType, Token
from linked_list import print_ll


def validate_quotes(line):
	'''Checks whether single and double quotes were closed correctly or not'''
	quote_type = None
	for c in line:
		if quote_type is None and (c == '"' or c == "'"):
			quote_type = c
		elif quote_type == c:
			quote_type = None
	return quote_type is None


def check_token_rules(token_list: Token):
	iter = token_list
	while iter is not None:
		if iter.type == TokenType.PIPE:
			if (iter.prev is None) or (iter.next.type != TokenType.STRING) or (iter.next is None):
				return False
		elif iter.type == TokenType.APPEND_TO:
			if (iter.next is None) or (iter.next.type != TokenType.STRING):
				return False
		elif iter.type == TokenType.REDIR_TO:
			if (iter.next is None) or (iter.next.type != TokenType.STRING):
				return False
		elif iter.type == TokenType.HERE_DOC:
			if (iter.next is None) or (iter.next.type != TokenType.STRING):
				return False
		elif iter.type == TokenType.REDIR_FROM:
			if (iter.next is None) or (iter.next.type != TokenType.STRING):
				return False
		iter = iter.next
	return True


def parse(line):
	if not validate_quotes(line):
		print('SyntaxError: unclosed quotes')
		return
	var_idxs_to_expand = detect_expansions(line)
	token_list = tokenize(line)
	if not check_token_rules(token_list):
		print('SyntaxError: invalid tokens')
		return
	expanded_token_list = expand(token_list, var_idxs_to_expand)
	return expanded_token_list

	
def interactive():
	while True:
		line = input('$ ')
		tokens = parse(line)
		print_ll(tokens)


def main():
	interactive()


if __name__ == '__main__':
	main()
