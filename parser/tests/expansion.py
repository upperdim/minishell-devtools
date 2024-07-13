from expansion import detect_expansions


def expansion_detection_tests():
	print('Running expansion detection tests...')

	expansion_detection_tests = [
		['$2$ ', []],
		['$2$ $a x', [2]],
		['a$$b', [0]],
		['a$b$c123$$$$$a$2$ x', [0, 1, 2, 4, 6]],
		["a$$b \" a$$b \" a$$b ' a$$b ' a$$b", [0, 2, 4, 8]],
	]

	failed_count = 0
	test_count = 0
	for i, test in enumerate(expansion_detection_tests):
		test_count += 1
		# print(f'i={i} test case = {test[0]}')
		actual = detect_expansions(test[0])
		expected = test[1]
		if actual != expected:
			failed_count += 1
			print(f'\nFailed test {i + 1}')
			print(f'Test case = {test[0]}')
			print(f'Actual    = {actual}')
			print(f'Expected  = {expected}')
	if failed_count == 0:
		print(f'OK ({test_count})')
	else:
		print(f'\nFailed {failed_count} tests.')
