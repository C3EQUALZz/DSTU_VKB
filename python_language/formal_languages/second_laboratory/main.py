"""
Пример ввода:
S -> R
S -> T
R -> pX
R -> paR
R -> paT
T -> Tg
T -> g
X -> aXb
Y -> aYa
Y -> y
exit
"""
from python_language.formal_languages.first_laboratory import is_context_free
from python_language.formal_languages.useful_functions import get_rules_from_console


def check_exist(grammar_rules: dict[str, list[str]]) -> bool:
    """
    Проверка на существование языка КС-грамматики
    """
    reachable_symbols = {"S"}

    def update_reachable_symbols(symbols: set[str]) -> None:
        """
        Обновляет нашей множество достижимых символов
        """
        nonlocal reachable_symbols
        for symbol in symbols:
            if symbol not in reachable_symbols:
                reachable_symbols.add(symbol)

    def factory(productions_inner: list[str]) -> bool | None:
        """
        Здесь используется фабрика, которая все запускает для удобства
        """
        for production_inner in productions_inner:
            # Если все символы из правила уже достижимы, добавляем не терминал в множество
            if all(symbol in reachable_symbols for symbol in production_inner):
                update_reachable_symbols({non_terminal})
                return True

    # Пока мы добавляем новые символы в множество достижимых, продолжаем итерации
    changed = True
    while changed:
        changed = False
        for non_terminal, productions in grammar_rules.items():
            changed = factory(productions)

    # Если стартовый символ достижим, значит язык существует
    return "S" in reachable_symbols


def main() -> str:
    # Считываем информацию с консоли
    rules = get_rules_from_console()

    if is_context_free(rules):
        return (f"1)Введена КС - грамматика\n2)"
                f"{'Язык существует' if check_exist(rules) else 'Язык не существует'}")
    return "1)Введенная грамматика не является КС-грамматикой "


if __name__ == "__main__":
    print(main())
