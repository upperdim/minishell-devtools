from expansion_var import detect_var_expansions, expand_var
from expansion_tilda import detect_tilda_expansions, expand_tilda
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
	tilda_idxs_to_expand = detect_tilda_expansions(line)
	var_idxs_to_expand = detect_var_expansions(line)
	token_list = tokenize(line)
	if not check_token_rules(token_list):
		print('SyntaxError: invalid tokens')
		return
	token_list = expand_tilda(token_list, tilda_idxs_to_expand)
	token_list = expand_var(token_list, var_idxs_to_expand)
	return token_list

	
def interactive():
	while True:
		line = input('$ ')
		tokens = parse(line)
		print_ll(tokens)


def main():
	interactive()


if __name__ == '__main__':
	main()
