from tokenizer import Token


def print_ll(head: Token, lines_prefix: str=''):
	if head is None:
		print(f'{lines_prefix}<null node>')
	iter = head
	while iter is not None:
		print(f'{lines_prefix}{iter.type}: ({iter.val})')
		iter = iter.next
