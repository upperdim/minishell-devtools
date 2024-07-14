from test_parser import quote_validation_tests
from test_tokenizer import tokenizer_tests
from test_expansion_var import var_expansion_detection_tests
from test_expansion_tilda import tilda_expansion_detection_tests
from test_linked_list import ll_test_1, ll_test_2


def test_all():
	# ll_test_1()
	# ll_test_2()
	quote_validation_tests()
	tokenizer_tests()
	var_expansion_detection_tests()
	tilda_expansion_detection_tests()


if __name__ == '__main__':
	test_all()
