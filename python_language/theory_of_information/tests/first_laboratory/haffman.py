# https://huffman.ooz.ie/

import pytest
from python_language.theory_of_information.models.first_laboratory import Huffman


def test_minimal_correct():
    assert Huffman.encode("abcdabc") == {"a": "01", "b": "10", "c": "11", "d": "00"}


def test_abracadabra():
    assert Huffman.encode("abracadabra") == {'a': '0', 'b': '111', 'c': '1100', 'd': '1101', 'r': '10'}


def test_one_symbol():
    assert Huffman.encode("a") == {"a": "0"}
    assert Huffman.encode("b") == {"b": "0"}
    assert Huffman.encode("c") == {"c": "0"}


def test_identical_chars():
    assert Huffman.encode("aaaaaaaa") == {"a": "0"}
    assert Huffman.encode("bbbbb") == {"b": "0"}
    assert Huffman.encode("ccccccccccccccccccccccccccc") == {"c": "0"}


def test_empty_string():
    assert Huffman.encode("") == {}


if __name__ == "__main__":
    pytest.main()
