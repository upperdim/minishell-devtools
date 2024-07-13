import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from tokenizer import  TokenType, Token, add_token
from linked_list import  print_ll


def ll_test_1():
	print(f'Runnig linked list test #1:')
	n3 = Token(TokenType.STRING, "!", None, None)
	n2 = Token(TokenType.STRING, "world", n3, None)
	n1 = Token(TokenType.STRING, "hello", n2, None)
	n2.prev = n1
	print_ll(n1)
	print_ll(n1)

def ll_test_2():
	print(f'Runnig linked list test #2:')
	head = None
	print_ll(head)
	head = add_token(head, Token(TokenType.STRING, "one", None, None))
	print_ll(head)
	head = add_token(head, Token(TokenType.STRING, "two", None, None))
	print_ll(head)
	head = add_token(head, Token(TokenType.STRING, "three", None, None))
	print_ll(head)
