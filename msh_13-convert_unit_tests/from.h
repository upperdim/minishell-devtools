# ifndef TEST
#  define TEST_CASE ""
#  define EXPECTED {NULL}
#  define STR_INDEX {-1}
#  define EXP_TYPES {-1}
#  define E_COUNT 1
# endif
# if TEST == 1
#  define TEST_CASE ""
#  define EXPECTED {NULL}
#  define STR_INDEX {-1}
#  define EXP_TYPES {-1}
#  define E_COUNT 1
# elif TEST == 2
#  define TEST_CASE NULL
#  define EXPECTED {NULL}
#  define STR_INDEX {-1}
#  define EXP_TYPES {-1}
#  define E_COUNT 1
# elif TEST == 3
#  define TEST_CASE "echo Hello World"
#  define EXPECTED {"echo", "Hello", "World", NULL}
#  define STR_INDEX {0, 1, 2, -1}
#  define EXP_TYPES {STRING, STRING, STRING, -1}
#  define E_COUNT 4
# elif TEST == 4
#  define TEST_CASE "echo \"Hello  World\""
#  define EXPECTED {"echo", "Hello  World", NULL}
#  define STR_INDEX {0, 1, -1}
#  define EXP_TYPES {STRING, DOUBLE_QUOTES, -1}
#  define E_COUNT 3
# elif TEST == 5
#  define TEST_CASE "echo \"Hello' World\""
#  define EXPECTED {"echo", "Hello' World", NULL}
#  define STR_INDEX {0, 1, -1}
#  define EXP_TYPES {STRING, DOUBLE_QUOTES, -1}
#  define E_COUNT 3
# elif TEST == 6
#  define TEST_CASE "echo \"Hello\" World\""
#  define EXPECTED {"echo", "Hello", "World\"", NULL}
#  define STR_INDEX {0, 1, 2, -1}
#  define EXP_TYPES {STRING, DOUBLE_QUOTES, STRING, -1}
#  define E_COUNT 4
# elif TEST == 7 
#  define TEST_CASE "echo Hello\" World"
#  define EXPECTED {"echo", "Hello\"", "World", NULL}
#  define STR_INDEX {0, 1, 2, -1}
#  define EXP_TYPES {STRING, STRING, STRING, -1}
#  define E_COUNT 4
# elif TEST == 8
#  define TEST_CASE "echo \"Hello\"World"
#  define EXPECTED {"echo", "Hello", "World", NULL}
#  define STR_INDEX {0, 1, 1, -1}
#  define EXP_TYPES {STRING, DOUBLE_QUOTES, STRING, -1}
#  define E_COUNT 4
# elif TEST == 9
#  define TEST_CASE "echo Hello\"World\"       "
#  define EXPECTED {"echo", "Hello", "World", NULL}
#  define STR_INDEX {0, 1, 1, -1}
#  define EXP_TYPES {STRING, STRING, DOUBLE_QUOTES, -1}
#  define E_COUNT 4
# elif TEST == 10
#  define TEST_CASE "echo              Hello\"World\"'stuck'        "
#  define EXPECTED {"echo", "Hello", "World", "stuck", NULL}
#  define STR_INDEX {0, 1, 1, 1, -1}
#  define EXP_TYPES {STRING, STRING, DOUBLE_QUOTES, SINGLE_QUOTES, -1}
#  define E_COUNT 5
# elif TEST == 11
#  define TEST_CASE "ec ho\"  'Hello  \"World'  x "
#  define EXPECTED {"ec", "ho", "  'Hello  ", "World'", "x", NULL}
#  define STR_INDEX {0, 1, 1, 1, 2, -1}
#  define EXP_TYPES {STRING, STRING, DOUBLE_QUOTES, STRING, STRING, -1}
#  define E_COUNT 6
# elif TEST == 12
#  define TEST_CASE "\"'\"''\"'\""
#  define EXPECTED {"'", "", "'", NULL}
#  define STR_INDEX {0, 0, 0, -1}
#  define EXP_TYPES {DOUBLE_QUOTES, SINGLE_QUOTES, DOUBLE_QUOTES, -1}
#  define E_COUNT 4
# elif TEST == 13
#  define TEST_CASE "a\"'123'456\""
#  define EXPECTED {"a", "'123'456", NULL}
#  define STR_INDEX {0, 0, -1}
#  define EXP_TYPES {STRING, DOUBLE_QUOTES, -1}
#  define E_COUNT 3
# elif TEST == 14
#  define TEST_CASE "\"'123'456\""
#  define EXPECTED {"'123'456", NULL}
#  define STR_INDEX {0, -1}
#  define EXP_TYPES {DOUBLE_QUOTES, -1}
#  define E_COUNT 2
# elif TEST == 15
#  define TEST_CASE "\"'\""
#  define EXPECTED {"'", NULL}
#  define STR_INDEX {0, -1}
#  define EXP_TYPES {DOUBLE_QUOTES, -1}
#  define E_COUNT 2
# elif TEST == 16
#  define TEST_CASE "''"
#  define EXPECTED {"", NULL}
#  define STR_INDEX {0, -1}
#  define EXP_TYPES {SINGLE_QUOTES, -1}
#  define E_COUNT 2
# elif TEST == 17
#  define TEST_CASE "\"\""
#  define EXPECTED {"", NULL}
#  define STR_INDEX {0, -1}
#  define EXP_TYPES {DOUBLE_QUOTES, -1}
#  define E_COUNT 2
# elif TEST == 18
#  define TEST_CASE "'\"'"
#  define EXPECTED {"\"", NULL}
#  define STR_INDEX {0, -1}
#  define EXP_TYPES {SINGLE_QUOTES, -1}
#  define E_COUNT 2
# elif TEST == 19
#  define TEST_CASE "''\"'\""
#  define EXPECTED {"", "'", NULL}
#  define STR_INDEX {0, 0, -1}
#  define EXP_TYPES {SINGLE_QUOTES, DOUBLE_QUOTES, -1}
#  define E_COUNT 3
# elif TEST == 20
#  define TEST_CASE "\"no clue of ''what other test   \"to do'"
#  define EXPECTED {"no clue of ''what other test   ", "to", "do'", NULL}
#  define STR_INDEX {0, 0, 1, -1}
#  define EXP_TYPES {DOUBLE_QUOTES, STRING, STRING, -1}
#  define E_COUNT 4
# elif TEST == 21
#  define TEST_CASE "echo hi | cat -e"
#  define EXPECTED {"echo", "hi", "|", "cat", "-e", NULL}
#  define STR_INDEX {0, 1, 2, 3, 4, -1}
#  define EXP_TYPES {STRING, STRING, PIPE, STRING, STRING, -1}
#  define E_COUNT 6
# elif TEST == 22
#  define TEST_CASE "echo hi|cat -e"
#  define EXPECTED {"echo", "hi", "|", "cat", "-e", NULL}
#  define STR_INDEX {0, 1, 2, 3, 4, -1}
#  define EXP_TYPES {STRING, STRING, PIPE, STRING, STRING, -1}
#  define E_COUNT 6
# elif TEST == 23
#  define TEST_CASE "echo \"hi|cat\" -e"
#  define EXPECTED {"echo", "hi|cat", "-e", NULL}
#  define STR_INDEX {0, 1, 2, -1}
#  define EXP_TYPES {STRING, DOUBLE_QUOTES, STRING, -1}
#  define E_COUNT 4
# elif TEST == 24
#  define TEST_CASE "echo hi\"|\"cat -e"
#  define EXPECTED {"echo", "hi", "|", "cat", "-e", NULL}
#  define STR_INDEX {0, 1, 1, 1, 2, -1}
#  define EXP_TYPES {STRING, STRING, DOUBLE_QUOTES, STRING, STRING, -1}
#  define E_COUNT 6
# elif TEST == 25
#  define TEST_CASE "echo\" Hello World\""
#  define EXPECTED {"echo", " Hello World", NULL}
#  define STR_INDEX {0, 0, -1}
#  define EXP_TYPES {STRING, DOUBLE_QUOTES, -1}
#  define E_COUNT 3
# elif TEST == 26
#  define TEST_CASE "export VAR=\"echo hi | cat\""
#  define EXPECTED {"export", "VAR=echo hi | cat", NULL}
#  define STR_INDEX {0, 1, 1, -1}
#  define EXP_TYPES {STRING, STRING, DOUBLE_QUOTES, -1}
#  define E_COUNT 4
# endif