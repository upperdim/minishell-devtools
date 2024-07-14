from tokenizer import TokenType, Token


def detect_tilda_expansions(line):
	def is_eligible_for_expansion(line, i, quote_type):
		# Only tildas will be expanded (duh)
		if line[i] != '~':
			return False
		# Tildas inside any type of quotes won't be expanded
		if quote_type is not None:
			return False
		# If there is a previous char, it must be space
		if i > 0 and line[i - 1] != ' ':
			return False
		# Next char can only be space or forward slash
		if i + 1 < len(line) and line[i + 1] not in " /":
			return False
		return True
		
	tilda_idxs_to_expand = []
	tilda_idx = 0
	quote_type = None
	i = 0
	while i < len(line):
		if quote_type is None and (line[i] == "'" or line[i] == '"'):
			quote_type = line[i]
		elif line[i] == quote_type:
			quote_type = None
		elif line[i] == '~':
			if is_eligible_for_expansion(line, i, quote_type):
				tilda_idxs_to_expand.append(tilda_idx)
			tilda_idx += 1
		i += 1
	return tilda_idxs_to_expand


def expand_tilda(token_list: Token, tilda_idxs_to_expand):
	def get_tilda_value():
		'''Fetch tilda value from os'''
		return '/home/exampleusername'
	
	def str_replace_section(s, start_idx, end_idx, replace_with):
		'''Replace string `s` from `start_idx` to `end_idx` inclusive with `replace_with`'''
		new = ''
		new += s[:start_idx]
		new += replace_with
		new += s[end_idx:]
		return new

	tilda_idx = 0
	idx_idx = 0
	iter = token_list
	while iter is not None:
		if iter.type != TokenType.STRING:
			iter = iter.next
			continue
		i = 0
		while i < len(iter.val):
			if iter.val[i] == '~':
				if len(tilda_idxs_to_expand) > idx_idx and tilda_idx == tilda_idxs_to_expand[idx_idx]:
					iter.val = str_replace_section(iter.val, i, i, get_tilda_value())
					idx_idx += 1
				tilda_idx += 1
			i += 1
		iter = iter.next
	return token_list
