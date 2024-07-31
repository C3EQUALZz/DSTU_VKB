import pytest
from python_language.theory_of_information.models.second_laboratory import LZ78, TokenLZ78


@pytest.fixture()
def algorithm():
    return LZ78()


def parametrize_compress_test_cases():
    return [
        ("ЗЕЛЕНАЯ_ЗЕЛЕНЬ_ЗЕЛЕНЕЕТ", [(0, 'З'), (0, 'Е'), (0, 'Л'), (2, 'Н'), (0, 'А'), (0, "Я"),
                                     (0, "_"), (1, "Е"), (3, "Е"), (0, "Н"), (0, "Ь"), (7, "З"),
                                     (2, "Л"), (4, "Е"), (2, "Т")])
    ]


def parametrize_decompress_test_cases():
    return [
        ([TokenLZ78(0, 'З'), TokenLZ78(0, 'Е'), TokenLZ78(0, 'Л'), TokenLZ78(2, 'Н'), TokenLZ78(0, 'А'),
          TokenLZ78(0, "Я"), TokenLZ78(0, "_"), TokenLZ78(1, "Е"), TokenLZ78(3, "Е"), TokenLZ78(0, "Н"),
          TokenLZ78(0, "Ь"), TokenLZ78(7, "З"), TokenLZ78(2, "Л"), TokenLZ78(4, "Е"), TokenLZ78(2, "Т")],
         "ЗЕЛЕНАЯ_ЗЕЛЕНЬ_ЗЕЛЕНЕЕТ")
    ]


@pytest.mark.parametrize("text,expected", parametrize_compress_test_cases())
def test_lz78_compression(algorithm, text, expected):
    compressed = algorithm.compress(text)
    assert compressed == expected


@pytest.mark.parametrize("text,expected", parametrize_decompress_test_cases())
def test_lz78_decompression(algorithm, text, expected):
    decompressed = algorithm.decompress(text)
    assert decompressed == expected


if __name__ == "__main__":
    pytest.main()
