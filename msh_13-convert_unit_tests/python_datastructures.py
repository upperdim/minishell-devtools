STRING = 1
PIPE = 2


test_cases = [
	{
		"test_case"	: "echo Hello World",
		"expected"	: ["echo", "Hello", "World"],
		"str_index"	: [0, 1, 2],
		"exp_types"	: [STRING, STRING, STRING],
	},
	{
		"test_case"	: "echo \"Hello  World\"",
		"expected"	: ["echo", "Hello  World"],
		"str_index"	: [0, 1],
		"exp_types"	: [STRING, STRING],
	},
	{
		"test_case"	: "echo \"Hello' World\"",
		"expected"	: ["echo", "Hello' World"],
		"str_index"	: [0, 1],
		"exp_types"	: [STRING, STRING],
	},
	{
		"test_case"	: "echo \"Hello\" World\"",
		"expected"	: ["echo", "Hello", "World\""],
		"str_index"	: [0, 1, 2],
		"exp_types"	: [STRING, STRING, STRING],
	},
	{
		"test_case"	: "echo Hello\" World",
		"expected"	: ["echo", "Hello\"", "World"],
		"str_index"	: [0, 1, 2],
		"exp_types"	: [STRING, STRING, STRING],
	},
	{
		"test_case"	: "echo \"Hello\"World",
		"expected"	: ["echo", "Hello", "World"],
		"str_index"	: [0, 1, 1],
		"exp_types"	: [STRING, STRING, STRING],
	},
	{
		"test_case"	: "echo Hello\"World\"       ",
		"expected"	: ["echo", "Hello", "World"],
		"str_index"	: [0, 1, 1],
		"exp_types"	: [STRING, STRING, STRING],
	},
	{
		"test_case"	: "echo              Hello\"World\"'stuck'        ",
		"expected"	: ["echo", "Hello", "World", "stuck"],
		"str_index"	: [0, 1, 1, 1],
		"exp_types"	: [STRING, STRING, STRING, STRING],
	},
	{
		"test_case"	: "ec ho\"  'Hello  \"World'  x ",
		"expected"	: ["ec", "ho", "  'Hello  ", "World'", "x"],
		"str_index"	: [0, 1, 1, 1, 2],
		"exp_types"	: [STRING, STRING, STRING, STRING, STRING],
	},
	# 10
	{
		"test_case"	: "\"'\"''\"'\"",
		"expected"	: ["'", "", "'"],
		"str_index"	: [0, 0, 0],
		"exp_types"	: [STRING, STRING, STRING],
	},
	{
		"test_case"	: "a\"'123'456\"",
		"expected"	: ["a", "'123'456"],
		"str_index"	: [0, 0],
		"exp_types"	: [STRING, STRING],
	},
	{
		"test_case"	: "\"'123'456\"",
		"expected"	: ["'123'456"],
		"str_index"	: [0],
		"exp_types"	: [STRING],
	},
	{
		"test_case"	: "\"'\"",
		"expected"	: ["'"],
		"str_index"	: [0],
		"exp_types"	: [STRING],
	},
	{
		"test_case"	: "''",
		"expected"	: [""],
		"str_index"	: [0],
		"exp_types"	: [STRING],
	},
	# 15
	{
		"test_case"	: "\"\"",
		"expected"	: [""],
		"str_index"	: [0],
		"exp_types"	: [STRING],
	},
	{
		"test_case"	: "'\"'",
		"expected"	: ["\""],
		"str_index"	: [0],
		"exp_types"	: [STRING],
	},
	{
		"test_case"	: "''\"'\"",
		"expected"	: ["", "'"],
		"str_index"	: [0, 0],
		"exp_types"	: [STRING, STRING],
	},
	{
		"test_case"	: "\"no clue of ''what other test   \"to do'",
		"expected"	: ["no clue of ''what other test   ", "to", "do'"],
		"str_index"	: [0, 0, 1],
		"exp_types"	: [STRING, STRING, STRING],
	},
	{
		"test_case"	: "echo hi | cat -e",
		"expected"	: ["echo", "hi", "|", "cat", "-e"],
		"str_index"	: [0, 1, 2, 3, 4],
		"exp_types"	: [STRING, STRING, PIPE, STRING, STRING],
	},
	# 20
	{
		"test_case"	: "echo hi|cat -e",
		"expected"	: ["echo", "hi", "|", "cat", "-e"],
		"str_index"	: [0, 1, 2, 3, 4],
		"exp_types"	: [STRING, STRING, PIPE, STRING, STRING],
	},
	{
		"test_case"	: "echo \"hi|cat\" -e",
		"expected"	: ["echo", "hi|cat", "-e"],
		"str_index"	: [0, 1, 2],
		"exp_types"	: [STRING, STRING, STRING],
	},
	{
		"test_case"	: "echo hi\"|\"cat -e",
		"expected"	: ["echo", "hi", "|", "cat", "-e"],
		"str_index"	: [0, 1, 1, 1, 2],
		"exp_types"	: [STRING, STRING, STRING, STRING, STRING],
	},
	{
		"test_case"	: "echo\" Hello World\"",
		"expected"	: ["echo", " Hello World"],
		"str_index"	: [0, 0],
		"exp_types"	: [STRING, STRING],
	},
	# TODO: there was an error in this test case (TEST 26 in C)
	{ 
		"test_case"	: "export VAR=\"echo hi | cat\"",
		"expected"	: ["export", "VAR", "=echo hi | cat"],
		"str_index"	: [0, 1, 1],
		"exp_types"	: [STRING, STRING, STRING],
	},
]


new_expecteds = [] # convert above structure into a str form
for test_case in test_cases:
	expected = test_case["expected"]
	word_indexes = test_case["str_index"]
	
	word_count = word_indexes[-1] + 1
	new_expected = ["" for x in range(word_count)]

	for i in range(len(word_indexes)):
		current_word_idx = word_indexes[i]
		new_expected[current_word_idx] += expected[i]
	
	new_expecteds.append(new_expected)


print('\n\n\n')
for i, new_expected in enumerate(new_expecteds):
	print(f'{new_expected}')
