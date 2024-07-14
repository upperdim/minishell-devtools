import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from expansion_tilda import detect_tilda_expansions


def tilda_expansion_detection_tests():
	tilda_expansion_detection_tests = [
		['~ ', [0]],
		[' " ~ " ', []],
		[" ' ~ ' ", []],
		[' a~ ', []],
		[" ~a ", []],
		[" ~/ ", [0]],
		[" ~/a ", [0]],
	]

	print(f'Running {len(tilda_expansion_detection_tests)} tilda expansion detection tests...')

	failed_count = 0
	test_count = 0
	for i, test in enumerate(tilda_expansion_detection_tests):
		test_count += 1
		# print(f'i={i} test case = {test[0]}')
		actual = detect_tilda_expansions(test[0])
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
