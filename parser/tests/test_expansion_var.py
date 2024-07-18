import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from expansion_var import detect_var_expansions


def var_expansion_detection_tests():
	var_expansion_detection_tests = [
		['$2$ ', []],
		['$2$ $a x', [2]],
		['  $?  ', [0]],
		['a$$b', [0]],
		['a$b$c123$$$$$a$2$ x', [0, 1, 2, 4, 6]],
		["a$$b \" a$$b \" a$$b ' a$$b ' a$$b", [0, 2, 4, 8]],
	]

	print(f'Running {len(var_expansion_detection_tests)} variable expansion detection tests...')

	failed_count = 0
	for i, test in enumerate(var_expansion_detection_tests):
		# print(f'i={i} test case = {test[0]}')
		actual = detect_var_expansions(test[0])
		expected = test[1]
		if actual != expected:
			failed_count += 1
			print(f'\nFailed test {i + 1}')
			print(f'Test case = {test[0]}')
			print(f'Actual    = {actual}')
			print(f'Expected  = {expected}')
	if failed_count == 0:
		print(f'OK')
	else:
		print(f'\nFailed {failed_count} tests.')
