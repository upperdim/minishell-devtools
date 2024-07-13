from tokenizer import TokenType, Token


def is_digit(c):
	return c >= '0' and c <= '9'


def is_valid_var_expansion_char(c):
	return (c == '_' 
		or (c >= 'a' and c <= 'z')
		or (c >= 'A' and c <= 'Z')
		or (c >= '0' and c <= '9'))


def detect_expansions(line):
	def is_eligible_for_expansion(line, s, is_in_single_quote, var_idx):
		if line[s] == "'":
			is_in_single_quote = not is_in_single_quote
			s += 1
			return False, s, is_in_single_quote, var_idx
		if line[s] != '$':
			s += 1
			return False, s, is_in_single_quote, var_idx
		if is_in_single_quote:
			var_idx += 1
			s += 1
			return False, s, is_in_single_quote, var_idx
		if s + 1 < len(line) and is_digit(line[s + 1]):
			s += 2
			var_idx += 1
			return False, s, is_in_single_quote, var_idx
		return True, s, is_in_single_quote, var_idx

	vars_idxs_to_expand = []
	var_idx = 0
	is_in_single_quote = False
	s = 0
	while s < len(line):
		is_eligible, s, is_in_single_quote, var_idx = is_eligible_for_expansion(line, s, is_in_single_quote, var_idx)
		if not is_eligible:
			continue
		e = s + 1
		while e < len(line) and is_valid_var_expansion_char(line[e]):
			e += 1
		if e != s + 1:
			vars_idxs_to_expand.append(var_idx)
		elif line[e] == '$':
			vars_idxs_to_expand.append(var_idx)
			var_idx += 2
			s += 2
			continue
		s = e
		var_idx += 1
	return vars_idxs_to_expand


def expand(token_list: Token, var_idxs_to_expand):
	def expand_replace(var_name):
		return 'i_am_' + var_name

	var_idx = 0
	idx_idx = 0
	iter = token_list
	while iter is not None:
		if iter.type == TokenType.STRING:
			i = 0
			while i < len(iter.val):
				if iter.val[i] == '$':
					if len(var_idxs_to_expand) > idx_idx and var_idx == var_idxs_to_expand[idx_idx]:
						e = i + 1
						while e < len(iter.val) and is_valid_var_expansion_char(iter.val[e]):
							e += 1
						# can put in a function, replaces idx i to e of old string section with a new one
						new_val = iter.val[:i]
						new_val += expand_replace(iter.val[i + 1:e])
						new_val += iter.val[e:]
						iter.val = new_val
						idx_idx += 1
					var_idx += 1
				i += 1
		iter = iter.next
	return token_list
