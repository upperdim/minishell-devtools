import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from tokenizer import  TokenType, Token, tokenize
from linked_list import  print_ll


def tokenizer_tests():
	def is_ll_equal_list(head: Token, token_list):
		i = 0
		iter = head
		while iter is not None:
			if iter.val != token_list[i][0] or iter.type != token_list[i][1]:
				return -1
			iter = iter.next
			i += 1
		if i != len(token_list):
			return -2
		return 1

	tests = [
		# Currently debugging
		# N/A
		
		# Split from redirecitons
		['echo asd>hello', 
   			[['echo', TokenType.STRING],
	   		['asd', TokenType.STRING],
			['>', TokenType.REDIR_TO],
			['hello', TokenType.STRING]
			]
		],
		['echo asd<hello',
   			[['echo', TokenType.STRING],
	   		['asd', TokenType.STRING],
			['<', TokenType.REDIR_FROM],
			['hello', TokenType.STRING]
			]
		],
		['echo asd>>hello',
   			[['echo', TokenType.STRING],
	   		['asd', TokenType.STRING],
			['>>', TokenType.APPEND_TO],
			['hello', TokenType.STRING]
			]
		],
		['echo asd<<hello',
   			[['echo', TokenType.STRING],
	   		['asd', TokenType.STRING],
			['<<', TokenType.HERE_DOC],
			['hello', TokenType.STRING],
			]
		],

		# Quote Adjacent Redirections
		# Exception: Redirections near quotes create their own words
		['cat <<" EOF"',
   			[['cat', TokenType.STRING],
	   		['<<', TokenType.HERE_DOC],
			[' EOF', TokenType.STRING],
			]
		],
		['cat <" EOF"',
   			[['cat', TokenType.STRING],
	   		['<', TokenType.REDIR_FROM],
			[' EOF', TokenType.STRING],
			]
		],
		['cat >>" EOF"',
   			[['cat', TokenType.STRING],
	   		['>>', TokenType.APPEND_TO],
			[' EOF', TokenType.STRING],
			]
		],
		['cat >" EOF"',
   			[['cat', TokenType.STRING],
	   		['>', TokenType.REDIR_TO],
			[' EOF', TokenType.STRING],
			]
		],
		['cat <<\' EOF\'',
   			[['cat', TokenType.STRING],
	   		['<<', TokenType.HERE_DOC],
			[' EOF', TokenType.STRING],
			]
		],
		['cat <\' EOF\'',
   			[['cat', TokenType.STRING],
	   		['<', TokenType.REDIR_FROM],
			[' EOF', TokenType.STRING],
			]
		],
		['cat >>\' EOF\'',
   			[['cat', TokenType.STRING],
	   		['>>', TokenType.APPEND_TO],
			[' EOF', TokenType.STRING],
			]
		],
		['cat >\' EOF\'',
   			[['cat', TokenType.STRING],
	   		['>', TokenType.REDIR_TO],
			[' EOF', TokenType.STRING],
			]
		],
		
		# Redirections w/ prefix & fd
		['cat hello<<" EOF"',
   			[['cat', TokenType.STRING],
	   		['hello', TokenType.STRING],
			['<<', TokenType.HERE_DOC],
			[' EOF', TokenType.STRING],
			]
		],
		['cat 123<<" EOF"',
   			[['cat', TokenType.STRING],
			['123<<', TokenType.HERE_DOC],
			[' EOF', TokenType.STRING],
			]
		],
		['cat hello123<<" EOF"',
   			[['cat', TokenType.STRING],
			['hello123', TokenType.STRING],
			['<<', TokenType.HERE_DOC],
			[' EOF', TokenType.STRING],
			]
		], # has to be entirely digits like above in order to get detected as a file descriptor for the redirection
		['cat hello1>file2name 123>file1name123>world<<" EOF"',
   			[['cat', TokenType.STRING],
			['hello1', TokenType.STRING],
			['>', TokenType.REDIR_TO],
			['file2name', TokenType.STRING],
			['123>', TokenType.REDIR_TO],
			['file1name123', TokenType.STRING],
			['>', TokenType.REDIR_TO],
			['world', TokenType.STRING],
			['<<', TokenType.HERE_DOC],
			[' EOF', TokenType.STRING],
			]
		],

		# Redirections w/ prefix & fd: RANGE CHECK
		['cat -12> filename',
   			[['cat', TokenType.STRING],
	   		['-12', TokenType.STRING],
			['>', TokenType.REDIR_TO],
			['filename', TokenType.STRING],
			]
		], # since - is not digit, negative numbers count as filenames
		['cat 2147483647> filename',
   			[['cat', TokenType.STRING],
	   		['2147483647>', TokenType.REDIR_TO],
			['filename', TokenType.STRING],
			]
		],
		['cat 2147483648> filename',
   			[['cat', TokenType.STRING],
	   		['2147483648', TokenType.STRING],
			['>', TokenType.REDIR_TO],
			['filename', TokenType.STRING],
			]
		],

		# Error handling for invalid inputs
		#
		# These will be labeled as SYNTAX ERRORs either after tokenization or maybe here in lexing process
		# If you have a reliable way of cutting them out, just stop processing and give error to user
		['cat << >> <" EOF"',
   			[['cat', TokenType.STRING],
	   		['<<', TokenType.HERE_DOC],
			['>>', TokenType.APPEND_TO],
			['<', TokenType.REDIR_FROM],
			[' EOF', TokenType.STRING],
			]
		],
		['cat <<>> <" EOF"',
   			[['cat', TokenType.STRING],
	   		['<<', TokenType.HERE_DOC],
			['>>', TokenType.APPEND_TO],
			['<', TokenType.REDIR_FROM],
			[' EOF', TokenType.STRING],
			]
		],

		# Expansion
		# TBA
		
		# Quotes & Spaces
		['export VAR="echo hi | cat"',
			[['export', TokenType.STRING],
			['VAR=echo hi | cat', TokenType.STRING],
			]
		],
		['echo "Hello"World',
   			[['echo', TokenType.STRING],
			['HelloWorld', TokenType.STRING],
			]
		],
		['echo Hello World',
   			[['echo', TokenType.STRING],
	   		['Hello', TokenType.STRING],
			['World', TokenType.STRING],
			]
		],
		['echo "Hello  World"',
   			[['echo', TokenType.STRING],
	   		['Hello  World', TokenType.STRING],
			]
		],
		['cat "hello" x',
			[['cat', TokenType.STRING],
			['hello', TokenType.STRING],
			['x', TokenType.STRING],
			]
		],
		['echo Hello"World"       ',
   			[['echo', TokenType.STRING],
	   		['HelloWorld', TokenType.STRING],
			]
		],
		['echo              Hello"World"\'stuck\'        ',
   			[['echo', TokenType.STRING],
	   		['HelloWorldstuck', TokenType.STRING],
			]
		],
		['"\'"\'\'"\'"',
			[["''", TokenType.STRING]]
		],
		['a"\'123\'456"',
   			[["a'123'456", TokenType.STRING]]
		],
		['"\'123\'456"',
   			[["'123'456", TokenType.STRING]]
		],
		['"\'"',
   			[["'", TokenType.STRING]]
		],
		["''",
   			[['', TokenType.STRING]]
		],
		['""',
   			[['', TokenType.STRING]]
		],
		['\'"\'',
   			[['"', TokenType.STRING]]
		],
		['\'\'"\'"',
   			[["", TokenType.STRING],
	   		["'", TokenType.STRING]
			]
		],
		['echo" Hello World"',
   			[["echo Hello World", TokenType.STRING]]
		],
		['"no clue of \'\'what other test   "to do',
   			[["no clue of ''what other test   to", TokenType.STRING],
	   		["do", TokenType.STRING],
			]
		],
		['" dog" cat',
   			[[" dog", TokenType.STRING],
	   		["cat", TokenType.STRING],
			]
		],
		['echo asd << "" << file2',
			[['echo', TokenType.STRING],
			['asd', TokenType.STRING],
			['<<', TokenType.HERE_DOC],
			['', TokenType.STRING],
			['<<', TokenType.HERE_DOC],
			['file2', TokenType.STRING],
			]
		],

		# Pipes
		['echo hi | cat -e',
   			[["echo", TokenType.STRING],
	   		["hi", TokenType.STRING],
			["|", TokenType.PIPE],
			["cat", TokenType.STRING],
			["-e", TokenType.STRING],
			]
		],
		['echo hi|cat -e',
   			[["echo", TokenType.STRING],
	   		["hi", TokenType.STRING],
			["|", TokenType.PIPE],
			["cat", TokenType.STRING],
			["-e", TokenType.STRING],
			]
		],
		['echo hi|cat"asd" -e',
   			[["echo", TokenType.STRING],
	   		["hi", TokenType.STRING],
			["|", TokenType.PIPE],
			["catasd", TokenType.STRING],
			["-e", TokenType.STRING],
			]
		],
		['echo "hi|cat" -e',
   			[["echo", TokenType.STRING],
	   		["hi|cat", TokenType.STRING],
			["-e", TokenType.STRING],
			]
		],
		['echo hi"|"cat -e',
   			[["echo", TokenType.STRING],
	   		["hi|cat", TokenType.STRING],
			["-e", TokenType.STRING],
			]
		],

		# Unclosed Quotes
		# ['ec ho"  \'Hello  "World\'  x ',
		# 	[['ec', TokenType.STRING],
		# 	["ho  'Hello  World'", TokenType.STRING],
		# 	['x', TokenType.STRING],
		# 	]
		# ],
		# ['echo >>"hi"\'x y ',
   		# 	[['echo', TokenType.STRING],
	   	# 	['>>', TokenType.APPEND_TO],
	   	# 	["hi'x", TokenType.STRING],
		# 	['y', TokenType.STRING],
		# 	]
		# ],
		# ['echo >>"hi"\'',
   		# 	[['echo', TokenType.STRING],
	   	# 	['>>', TokenType.APPEND_TO],
	   	# 	["hi'", TokenType.STRING],
		# 	]
		# ],
		# ['echo "Hello\' World"',
   		# 	[["echo", TokenType.STRING],
	  	# 	["Hello' World", TokenType.STRING],
		# 	]
		# ],
		# ['echo "Hello" World"',
   		# 	[["echo", TokenType.STRING],
	   	# 	['Hello', TokenType.STRING],
	   	# 	['World"', TokenType.STRING],
		# 	]
		# ],
		# ['echo Hello" World',
   		# 	[["echo", TokenType.STRING],
	   	# 	['Hello"', TokenType.STRING],
	   	# 	['World', TokenType.STRING],
		# 	]
		# ],
	]
	
	print(f'Running {len(tests)} tokenizer tests...')

	failed_count = 0
	test_count = 0
	for i, test in enumerate(tests):
		test_count += 1
		# print(f'i={i} test case = {test[0]}')
		actual_ll_head = tokenize(test[0])
		expected_list = test[1]
		is_equal = is_ll_equal_list(actual_ll_head, expected_list)
		if is_equal != 1:
			failed_count += 1
			print(f'\nFailed test {i + 1}')
			print(f'Test case = {test[0]}')
			print(f'Actual    = ')
			print_ll(actual_ll_head, '\t')
			print(f'Expected  = {expected_list}')
			if is_equal == -2:
				print(f'MISMATCHING TOKEN LIST SIZES')
	if failed_count == 0:
		print(f'OK ({test_count})')
	else:
		print(f'\nFailed {failed_count} tests.')
