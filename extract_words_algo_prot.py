# Tokenize shell input line words
#
# Tokenize words of a shell input line


from dataclasses import dataclass
from enum import Enum


@dataclass
class LineSplit:
	data: str
	word_idx: int
	is_enc_single_quote: bool=False
	is_enc_double_quote: bool=False


class QuoteType(Enum):
    SINGLE = 1
    DOUBLE = 2


@dataclass
class EnclosedSection:
	begin_idx: int
	end_idx: int
	quote_type: QuoteType


def filter_included_ranges(data):
	included_ranges = []
	for i, range1 in enumerate(data):
		included = False
		for j, range2 in enumerate(data):
			if i != j:  # Skip comparing the range with itself
				if range1.begin_idx >= range2.begin_idx and range1.end_idx <= range2.end_idx:
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


# I have a string in python. I want to split it from multiple separator characters. I want an option for each character to decide if it will be kept in the resultant splits. Write me the function.
# This is exactly the functionality that I want. However, I don't want you to use regex. Generate a code that doesn't use regex.
def ft_split_multi_keep(input_string, separators, keep_separators):
    """
    Splits a string based on multiple separators with an option to keep or discard each separator.
    
    Parameters:
    - input_string (str): The string to split.
    - separators (list of str): The list of separator characters.
    - keep_separators (list of bool): A list of boolean values indicating whether to keep the corresponding separator.
    
    Returns:
    - list of str: The list of split parts.
    """
    # Check if the lengths of separators and keep_separators are the same
    if len(separators) != len(keep_separators):
        raise ValueError("The length of separators and keep_separators must be the same")
    result = []
    current_part = []
    separators_set = set(separators)
    keep_separators_map = {sep: keep for sep, keep in zip(separators, keep_separators)}
    for char in input_string:
        if char in separators_set:
            # Append the current part to the result if it's not empty
            if current_part:
                result.append(''.join(current_part))
                current_part = []
            # Append the separator if it should be kept
            if keep_separators_map[char]:
                result.append(char)
        else:
            current_part.append(char)
    # Append any remaining part to the result
    if current_part:
        result.append(''.join(current_part))
    return result


# split str_section by spaces and add the splits into token_words. Ignores empty string splits
def line_to_splits(splits, str_section, word_indexes, word_idx):
	new_word_idx = word_idx
	at_least_1_elem = False
	for split in ft_split_multi_keep(str_section, [' ', '|'], [False, True]):
		splits.append(LineSplit(split, new_word_idx, False, False))
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
	separator_characters = [' ', '|']
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
				enclosed_sections.append(EnclosedSection(double_q_open_idx, idx, QuoteType.DOUBLE))
				double_q_encountered = False
			else:
				double_q_encountered = True
				double_q_open_idx = idx
		if single_quote_condition(line, idx, double_q_encountered):
			if single_q_encountered == True:
				enclosed_sections.append(EnclosedSection(single_q_open_idx, idx, QuoteType.SINGLE))
				single_q_encountered = False
			else:
				single_q_encountered = True
				single_q_open_idx = idx

	current_idx = 0
	for enclosed_section in filter_included_ranges(enclosed_sections):
		# Until enclosed section
		word_idx = line_to_splits(splits, line[current_idx:enclosed_section.begin_idx], word_indexes, word_idx)
		if enclosed_section.begin_idx > 0 and line[enclosed_section.begin_idx - 1] in separator_characters:
			word_idx += 1
		# Inside enclosed section
		splits.append(LineSplit(line[enclosed_section.begin_idx + 1:enclosed_section.end_idx], word_idx, True, True)) # todo; figure out which type of quote is the section enclosed by
		if enclosed_section.end_idx < len(line) - 1 and line[enclosed_section.end_idx + 1] in separator_characters:
			word_idx += 1
		# Setup it up for after enclosed section
		current_idx = enclosed_section.end_idx + 1
	# From last enclosed section to end of str
	word_idx = line_to_splits(splits, line[current_idx:len(line)], word_indexes, word_idx)
	return splits


def merge_splits_to_words(splits):
	word_count = splits[-1].word_idx + 1
	final_words = ["" for x in range(word_count)]
	for i in range(len(splits)):
		current_word_idx = splits[i].word_idx
		final_words[current_word_idx] += splits[i].data
	return (final_words)


# def separate_pipes(words_before):
# 	words_after = []
# 	for word in words_before:
# 		splits = ft_split(word, '|')
# 		# Remove whitespace near pipe symbols
# 		for i in range(len(splits)):
# 			splits[i] = splits[i].strip(' ')
# 		# Add | in-between
# 		for i in range(len(splits)):
# 			words_after.append(splits[i])
# 			# Except for the last index, it's not "in-between"
# 			if i != len(splits) - 1:
# 				words_after.append('|')
# 	return words_after


# first algorithm first, index words and merge them later
def create_words(line):
	splits = create_splits(line)
	words = merge_splits_to_words(splits)
	# words = separate_pipes(words) # old way of doing things. create_splits() handles pipes too now.
	return words


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
		['echo hi|cat"asd" -e', ['echo', 'hi', '|', 'catasd', '-e']],
		# IDEA 1: make an exception list of patterns that will be ignored by the rule that separates this quote
		# IDEA 2: just do another pass looking for redirection patterns and quotes. Can be done even in token linked list
		['cat <<" EOF"', ['cat', '<<', ' EOF']],  # redirections near quotes create their own words
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
		['"no clue of \'\'what other test   "to do\'', ["no clue of ''what other test   to", "do'"]],
		['echo hi | cat -e', ['echo', 'hi', '|', 'cat', '-e']],
		['echo hi|cat -e', ['echo', 'hi', '|', 'cat', '-e']],
		['echo "hi|cat" -e', ['echo', 'hi|cat', '-e']],
		['echo hi"|"cat -e', ['echo', 'hi|cat', '-e']],
		['echo" Hello World"', ['echo Hello World']],
	]

	def run_tests():
		failed_count = 0
		for i, test in enumerate(tests):
			actual = create_words(test[0])
			expected = test[1]
			if not is_string_list_equal(actual, expected):
				failed_count += 1
				print(f'\nFailed test {i + 1}')
				print(f'Test case = {test[0]}')
				print(f'Actual    = {actual}')
				print(f'Expected  = {expected}')
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
	# test_splitting()


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
