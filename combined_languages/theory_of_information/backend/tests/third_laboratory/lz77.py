import pytest

from combined_languages.theory_of_information.backend.fifth_semestr.third_laboratory import LZ77, TokenLZ77


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
        ([TokenLZ77(0, 0, 'c'), TokenLZ77(0, 0, 'a'), TokenLZ77(0, 0, 'b'),
          TokenLZ77(0, 0, 'r'), TokenLZ77(3, 1, 'c'), TokenLZ77(2, 1, 'd'),
          TokenLZ77(7, 4, 'r'), TokenLZ77(3, 5, 'd')], 'cabracadabrarrarrad'),

        ([TokenLZ77(0, 0, 'a'), TokenLZ77(0, 0, 'b'), TokenLZ77(2, 2, 'c'),
          TokenLZ77(4, 3, 'a'), TokenLZ77(2, 2, 'a')], 'ababcbababaa'),

        ([TokenLZ77(0, 0, 'a'), TokenLZ77(1, 1, 'c'), TokenLZ77(3, 4, 'b'),
          TokenLZ77(3, 3, 'a'), TokenLZ77(1, 2, 'c')], 'aacaacabcabaaac')
    ]


@pytest.mark.parametrize("text,expected", parametrize_compress_test_cases())
def test_lz77_compression(algorithm, text, expected):
    compressed = algorithm.compress(text)
    assert compressed == [TokenLZ77(*t) for t in expected]


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
