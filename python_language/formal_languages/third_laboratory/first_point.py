from typing import Generator, Any
from python_language.formal_languages.useful_functions import get_rules_from_console


def _processing_terminal_values(grammar_inner: dict[str, list[str]], symbol: str) -> Generator[str, Any, None]:
    """
    Обработка терминальных значений перед добавлением в стек
    """
    if symbol in grammar_inner:
        yield from (char for production in grammar_inner[symbol] for char in production if char.isupper())


def _find_reachable_symbols(grammar_inner: dict[str, list[str]], start_symbol: str) -> set[str | None]:
    """
    Ищем динамически, проходя все символы в стеке
    """
    # Множество достижимых символов
    reachable = set()
    # Стек для обхода символов
    stack = [start_symbol]

    while stack:
        symbol = stack.pop()
        if symbol not in reachable:
            reachable.add(symbol)
            # Обработка терминальных значений перед добавлением в стек
            if terminal_values := _processing_terminal_values(grammar_inner=grammar_inner, symbol=symbol):
                stack.extend(terminal_values)

    return reachable


def _create_new_grammar(grammar_inner: dict[str, list[str]], reachable_symbols: set[str | None]) -> dict[str, list[str]]:
    """
    Создаем новую грамматику, изменять grammar_inner не хочется, да эффективно, но я спать хочу
    """
    new_grammar: dict[str, list[str]] = {}
    for symbol, productions in grammar_inner.items():
        if symbol in reachable_symbols:
            new_productions: list[str] = []
            for production in productions:
                # Включаем только те продукции, которые содержат достижимые символы
                if all(char in reachable_symbols or not char.isupper() for char in production):
                    new_productions.append(production)
            if new_productions:
                new_grammar[symbol] = new_productions

    return new_grammar


def remove_unreachable_symbols(grammar_inner):
    """
    Реализация пункта а) по удалению ненужных символов
    """
    # Предполагается, что первый символ - стартовый
    start_symbol = list(grammar_inner.keys())[0]
    reachable_symbols = _find_reachable_symbols(grammar_inner, start_symbol)

    # Создание нового словаря грамматики с достижимыми символами
    return _create_new_grammar(grammar_inner=grammar_inner, reachable_symbols=reachable_symbols)


def main() -> None:
    new_grammar = remove_unreachable_symbols(get_rules_from_console())
    print("Новая грамматика без недостижимых символов:")
    print(new_grammar)


if __name__ == "__main__":
    main()
