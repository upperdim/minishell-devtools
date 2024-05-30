# Tokenize shell input line words
#
# Tokenize words of a shell input line

def filter_included_ranges(data):
    included_ranges = []
    for i, range1 in enumerate(data):
        included = False
        for j, range2 in enumerate(data):
            if i != j:  # Skip comparing the range with itself
                if range1[0] >= range2[0] and range1[1] <= range2[1]:
                    included = True
                    break
        if not included:
            included_ranges.append(range1)
    return included_ranges


def ft_split(s, c):
	"""split `s` by `c`, exclude empty string results"""
	splits = s.split(c)
	while("" in splits):
		splits.remove("")
	return splits


ALLOW_BACKSPACE_ESCAPING = True


def double_quote_condition(line, idx, single_q_encountered):
	if ALLOW_BACKSPACE_ESCAPING and idx > 0:
		return line[idx - 1] != "\\" and line[idx] == "\"" and single_q_encountered == False
	else:
		return line[idx] == "\"" and single_q_encountered == False


def single_quote_condition(line, idx, double_q_encountered):
	if ALLOW_BACKSPACE_ESCAPING and idx > 0:
		return line[idx - 1] != "\\" and line[idx] == "\'" and double_q_encountered == False
	else:
		return line[idx] == "\'" and double_q_encountered == False


def handle_quotes(line):
	token_words = []

	double_q_encountered = False
	single_q_encountered = False
	double_q_open_idx = -1
	single_q_open_idx = -1

	enclosed_sections = []

	for idx in range(len(line)):
		if double_quote_condition(line, idx, single_q_encountered):
			if double_q_encountered == True:
				enclosed_sections.append([double_q_open_idx, idx])
				double_q_encountered = False
			else:
				double_q_encountered = True
				double_q_open_idx = idx
		if single_quote_condition(line, idx, double_q_encountered):
			if single_q_encountered == True:
				enclosed_sections.append([single_q_open_idx, idx])
				single_q_encountered = False
			else:
				single_q_encountered = True
				single_q_open_idx = idx

	current_idx = 0
	for enclosed_section in filter_included_ranges(enclosed_sections):
		for split in ft_split(  line[current_idx:enclosed_section[0]], ' '  ):
			token_words.append(split)                                              # until enclosed section
		token_words.append(  line[enclosed_section[0] + 1:enclosed_section[1]]  )  # inside enclosed section
		current_idx = enclosed_section[1] + 1                                      # setup it up for after enclosed section
	for split in ft_split(  line[current_idx:len(line)], ' '):
		token_words.append(split)
	return token_words


def main():
	tests = [
		"",
		"  say  \"ec ho\"  \'Hello  \"World\'  x ",
		"\"\'\"\'\'\"\'\"",
		"a\"'123'456\"",
		"\"'123'456\"",
		"\"\'\"",
		"\'\'",
		"\"\"",
		"\'\"\'",
		"\'\'\"\'\"",
		"\"no clue of \'\'what other test   \"to do\'",
		"export VAR=\"echo  hi | cat\"",
		"echo\" hello World\"",             # todo: should be 'echo hello World'
		"echo' hello World'",               # todo: should be 'echo hello World'
		"echo\" hello World\"'asd'\"xyz\"", # todo: should be 'echo hello Worldasdxyz'
	]

	for test in tests:
		print(f'{test} becomes {handle_quotes(test)}')


if __name__ == '__main__':
	main()
