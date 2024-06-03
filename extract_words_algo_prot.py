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


# split str_section by spaces and add the splits into token_words. Ignores empty string splits
def split_to_words(token_words, str_section, word_indexes, word_idx):
	new_word_idx = word_idx
	at_least_1_elem = False
	for split in ft_split(str_section, ' '):
		token_words.append(split)
		word_indexes.append(new_word_idx)
		new_word_idx += 1
		at_least_1_elem = True
	if at_least_1_elem:
		new_word_idx -= 1
	return new_word_idx


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


def create_splits(line):
	splits = []
	word_indexes = []
	word_idx = 0

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
		word_idx = split_to_words(splits, line[current_idx:enclosed_section[0]], word_indexes, word_idx)  # until enclosed section
		if enclosed_section[0] > 0 and line[enclosed_section[0] - 1] == ' ':
			word_idx += 1
		splits.append(  line[enclosed_section[0] + 1:enclosed_section[1]]  )     # inside enclosed section
		word_indexes.append(word_idx)
		if enclosed_section[1] < len(line) - 1 and line[enclosed_section[1] + 1] == ' ':
			word_idx += 1
		current_idx = enclosed_section[1] + 1                                    # setup it up for after enclosed section
	word_idx = split_to_words(splits, line[current_idx:len(line)], word_indexes, word_idx)  # last enclosed section to end of str
	return splits, word_indexes


def create_final_words(splits, word_indexes):
	word_count = word_indexes[-1] + 1
	final_words = ["" for x in range(word_count)]
	for i in range(len(word_indexes)):
		current_word_idx = word_indexes[i]
		final_words[current_word_idx] += splits[i]
	return (final_words)


# first algorithm first, index words and merge them later
def create_words(line):
	_splits, _word_indexes = create_splits(line)
	return create_final_words(_splits, _word_indexes)


def jorge_c_tests():
	def is_string_list_equal(a, b):
		if len(a) != len(b):
			return False
		for i in range(len(a)):
			if a[i] != b[i]:
				return False
		return True
	
	print('\njorge_c_tests')
	# [test_case_str, [expected_output_list]]
	tests = [
		['_echo "Hello"World', ['_echo', 'HelloWorld']],
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
		['"no clue of \'\'what other test   "to do\'', ["no clue of ''what other test   to", "do'"]],
		['echo hi | cat -e', ['echo', 'hi', '|', 'cat', '-e']],
		['echo hi|cat -e', ['echo', 'hi', '|', 'cat', '-e']],
		['echo "hi|cat" -e', ['echo', 'hi|cat', '-e']],
		['echo hi"|"cat -e', ['echo', 'hi|cat', '-e']],
		['echo" Hello World"', ['echo Hello World']],
		['export VAR="echo hi | cat"', ['export', 'VAR=echo hi | cat']],
	]

	def run_tests():
		failed_count = 0
		for i, test in enumerate(tests):
			actual = create_words(test[0])
			expected = test[1]
			if not is_string_list_equal(actual, expected):
				failed_count += 1
				print(f'Failed test {i + 1}: actual = <{actual}>, expected = <{expected}>')
			# else:
			# 	print(f'Passed: actual = <{actual}>, expected = <{expected}>')
		if failed_count == 0:
			print(f'OK')
		else:
			print(f'Failed {failed_count} tests.')

	def test_splitting():
		for i, test in enumerate(tests):
			actual, word_idxs = create_splits(test[0])
			print(f'\nTest case = {test[0]}')
			print(f'Expected = {test[1]}')
			print(f'Actual = {actual}')
			print(f'Word indexes = {word_idxs}')

	run_tests()
	test_splitting()


# these tests are already included above
def original_python_tests():
	print('\noriginal_python_tests')
	tests = [
		"",
		"  say  \"ec ho\"  \'Hello  \"World\'  x ",
		"\"\'\"\'\'\"\'\"",  # todo: should be <''> (no space = merge them)
		"a\"'123'456\"", # todo: merge too
		"\"'123'456\"",
		"\"\'\"",
		"\'\'",
		"\"\"",
		"\'\"\'",
		"\'\'\"\'\"", # todo: merge
		"\"no clue of \'\'what other test   \"to do\'", # todo: "to" should merge with the left
		"export VAR=\"echo  hi | cat\"", # todo: last 2 should merge
		"echo\" hello World\"",             # todo: should be 'echo hello World'
		"echo' hello World'",               # todo: should be 'echo hello World'
		"echo\" hello World\"'asd'\"xyz\"", # todo: should be 'echo hello Worldasdxyz'
	]
	for test in tests:
		print(f'{test} becomes {create_words(test)}')


def main():
	# original_python_tests()
	jorge_c_tests()


if __name__ == '__main__':
	main()
