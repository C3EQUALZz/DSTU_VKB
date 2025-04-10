import pytest

from formal_languages.first_laboratory import (is_context_free,
                                               is_context_sensitive,
                                               is_left_linear, is_right_linear)


def test_left_linear_grammar_correct():
    set_of_terminals = {"a", "b", "$"}
    set_of_non_terminals = {"A", "Z", "S"}
    rules = {"S": ["Ab"], "A": ["Ab", "Za"], "Z": ["Za", "$"]}

    assert is_left_linear(
        set_of_terminals=set_of_terminals,
        set_of_non_terminals=set_of_non_terminals,
        grammar=rules,
    )


def test_left_linear_grammar_incorrect():
    set_of_terminals = {"a", "b", "c"}
    set_of_non_terminals = {"A", "S"}
    rules = {"S": ["aS", "bA"], "A": ["ε", "cA"]}

    assert not is_left_linear(
        set_of_terminals=set_of_terminals,
        set_of_non_terminals=set_of_non_terminals,
        grammar=rules,
    )


def test_right_linear_grammar_correct():
    set_of_terminals = {"a", "b", "c"}
    set_of_non_terminals = {"A", "S"}
    rules = {"S": ["aS", "bA"], "A": ["ε", "cA"]}

    assert is_right_linear(
        set_of_terminals=set_of_terminals,
        set_of_non_terminals=set_of_non_terminals,
        grammar=rules,
    )


def test_right_linear_grammar_correct_2():
    set_of_terminals = {"a", "b", "$"}
    set_of_non_terminals = {"A", "S", "Z"}
    rules = {"S": ["aS", "aA"], "A": ["bA", "bZ"], "Z": ["$"]}

    assert is_right_linear(
        set_of_terminals=set_of_terminals,
        set_of_non_terminals=set_of_non_terminals,
        grammar=rules,
    )


def test_right_linear_grammar_correct_3():
    set_of_terminals = {"a"}
    set_of_non_terminals = {"A", "S"}
    rules = {"S": ["aA", "a", "ε"], "A": ["a", "aA"]}

    assert is_right_linear(
        set_of_terminals=set_of_terminals,
        set_of_non_terminals=set_of_non_terminals,
        grammar=rules,
    )


def test_is_context_free_correct():
    set_of_terminals = {"a", "b"}
    set_of_non_terminals = {"A", "S"}
    rules = {"S": ["aSb", "ε"]}

    assert is_context_free(
        set_of_terminals=set_of_terminals,
        set_of_non_terminals=set_of_non_terminals,
        grammar=rules,
    )


def test_is_context_free_correct_2():
    set_of_terminals = {"a", "b", "c"}
    set_of_non_terminals = {"A", "S", "Q"}
    rules = {"S": ["aQb", "accb"], "Q": ["cSc"]}

    context_free = is_context_free(
        set_of_terminals=set_of_terminals,
        set_of_non_terminals=set_of_non_terminals,
        grammar=rules,
    )

    left_linear = is_left_linear(
        set_of_terminals=set_of_terminals,
        set_of_non_terminals=set_of_non_terminals,
        grammar=rules,
    )

    right_linear = is_right_linear(
        set_of_terminals=set_of_terminals,
        set_of_non_terminals=set_of_non_terminals,
        grammar=rules,
    )

    assert context_free and not left_linear and not right_linear


def test_is_context_sensitive_correct():
    set_of_terminals = {"a", "b", "c", "d"}
    set_of_non_terminals = {"A", "S", "B"}
    rules = {
        "S": ["aAS"],
        "AS": ["AAS"],
        "AAA": ["ABA"],
        "A": ["b"],
        "bBA": ["bcdA"],
        "bS": ["ba"],
    }

    context_free = is_context_free(
        set_of_terminals=set_of_terminals,
        set_of_non_terminals=set_of_non_terminals,
        grammar=rules,
    )

    left_linear = is_left_linear(
        set_of_terminals=set_of_terminals,
        set_of_non_terminals=set_of_non_terminals,
        grammar=rules,
    )

    right_linear = is_right_linear(
        set_of_terminals=set_of_terminals,
        set_of_non_terminals=set_of_non_terminals,
        grammar=rules,
    )

    context_sensitive = is_context_sensitive(
        set_of_terminals=set_of_terminals,
        set_of_non_terminals=set_of_non_terminals,
        grammar=rules,
    )

    assert context_sensitive and not all([context_free, left_linear, right_linear])


def test_is_type_zero():
    set_of_terminals = set()
    set_of_non_terminals = {"S"}
    rules = {"S": ["SS"], "SS": ["ε"]}

    context_free = is_context_free(
        set_of_terminals=set_of_terminals,
        set_of_non_terminals=set_of_non_terminals,
        grammar=rules,
    )

    left_linear = is_left_linear(
        set_of_terminals=set_of_terminals,
        set_of_non_terminals=set_of_non_terminals,
        grammar=rules,
    )

    right_linear = is_right_linear(
        set_of_terminals=set_of_terminals,
        set_of_non_terminals=set_of_non_terminals,
        grammar=rules,
    )

    context_sensitive = is_context_sensitive(
        set_of_terminals=set_of_terminals,
        set_of_non_terminals=set_of_non_terminals,
        grammar=rules,
    )

    assert not all([context_free, left_linear, right_linear, context_sensitive])


if __name__ == "__main__":
    pytest.main()
