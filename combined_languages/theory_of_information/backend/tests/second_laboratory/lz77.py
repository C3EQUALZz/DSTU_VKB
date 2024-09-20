import pytest
from python_language.theory_of_information.models.second_laboratory import LZ77
from python_language.theory_of_information.models.second_laboratory.lz77 import Token


@pytest.fixture()
def algorithm():
    return LZ77(window_size=13, lookahead_buffer_size=6)


def parametrize_compress_test_cases():
    return [
        ("ababcbababaa", [(0, 0, 'a'), (0, 0, 'b'), (2, 2, 'c'), (4, 3, 'a'), (2, 2, 'a')]),

        ("красная краска", [(0, 0, 'к'), (0, 0, 'р'), (0, 0, 'а'), (0, 0, 'с'), (0, 0, 'н'), (3, 1, 'я'), (0, 0, ' '),
                            (0, 0, 'к'), (0, 0, 'р'), (5, 1, 'с'), (4, 1, 'а')]),

        ("cabracadabrarrarrad", [(0, 0, 'c'), (0, 0, 'a'), (0, 0, 'b'), (0, 0, 'r'),
                                 (3, 1, 'c'), (2, 1, 'd'), (7, 4, 'r'), (3, 5, 'd')]),

        ("aacaacabcabaaac", [(0, 0, 'a'), (1, 1, 'c'), (3, 4, 'b'), (3, 3, 'a'), (1, 2, 'c')])
    ]


def parametrize_decompress_test_cases():
    return [
        ([Token(0, 0, 'c'), Token(0, 0, 'a'), Token(0, 0, 'b'),
          Token(0, 0, 'r'), Token(3, 1, 'c'), Token(2, 1, 'd'),
          Token(7, 4, 'r'), Token(3, 5, 'd')], 'cabracadabrarrarrad'),

        ([Token(0, 0, 'a'), Token(0, 0, 'b'), Token(2, 2, 'c'),
          Token(4, 3, 'a'), Token(2, 2, 'a')], 'ababcbababaa'),

        ([Token(0, 0, 'a'), Token(1, 1, 'c'), Token(3, 4, 'b'),
          Token(3, 3, 'a'), Token(1, 2, 'c')], 'aacaacabcabaaac')
    ]


@pytest.mark.parametrize("text,expected", parametrize_compress_test_cases())
def test_lz77_compression(algorithm, text, expected):
    compressed = algorithm.compress(text)
    assert compressed == [Token(*t) for t in expected]


@pytest.mark.parametrize("list_with_tokens,expected", parametrize_decompress_test_cases())
def test_lz77_decompression(algorithm, list_with_tokens, expected):
    decompressed = algorithm.decompress(list_with_tokens)
    assert decompressed == expected


def test_find_encoding_token(algorithm: LZ77):
    assert algorithm._find_encoding_token("abrarrarrad", "abracad").offset == 7
    assert algorithm._find_encoding_token("adabrarrarrad", "cabrac").length == 1
    assert algorithm._find_encoding_token("abc", "xyz").offset == 0
    with pytest.raises(ValueError):
        _ = algorithm._find_encoding_token("", "xyz").offset
    assert algorithm._find_encoding_token("abc", "").offset == 0


def test_match_length_from_index(algorithm: LZ77):
    assert algorithm._match_length_from_index("rarrad", "adabrar", 0, 4) == 5
    assert algorithm._match_length_from_index("adabrarrarrad", "cabrac", 0, 1) == 1


if __name__ == "__main__":
    pytest.main()
