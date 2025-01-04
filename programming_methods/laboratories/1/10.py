"""
Задача №50. Игра в пьяницу

В игре в пьяницу карточная колода раздается поровну двум игрокам. Далее они вскрывают по одной верхней карте, и тот,
чья карта старше, забирает себе обе вскрытые карты, которые кладутся под низ его колоды.
Тот, кто остается без карт – проигрывает.

Для простоты будем считать, что все карты различны по номиналу, а также, что самая младшая карта побеждает самую
старшую карту ("шестерка берет туза").

Игрок, который забирает себе карты, сначала кладет под низ своей колоды карту первого игрока, затем карту второго
игрока (то есть карта второго игрока оказывается внизу колоды).

Напишите программу, которая моделирует игру в пьяницу и определяет, кто выигрывает.
В игре участвует 10 карт, имеющих значения от 0 до 9, большая карта побеждает меньшую, карта со значением 0 побеждает карту 9.

Входные данные

Программа получает на вход две строки: первая строка содержит 5 чисел, разделенных пробелами — номера карт первого игрока,
вторая – аналогично 5 карт второго игрока. Карты перечислены сверху вниз, то есть каждая строка начинается с той карты,
которая будет открыта первой.

Выходные данные

Программа должна определить, кто выигрывает при данной раздаче, и вывести слово first или second,
после чего вывести количество ходов, сделанных до выигрыша.
Если на протяжении 106 ходов игра не заканчивается, программа должна вывести слово botva.
"""
from collections import deque
from typing import Union, Tuple


def play_game(first_deck: deque[str], second_deck: deque[str]) -> Union[str, Tuple[str, int]]:
    rounds = 0
    max_rounds = 1_000_000

    while first_deck and second_deck:
        rounds += 1
        first_card = first_deck.popleft()
        second_card = second_deck.popleft()

        if is_first_player_winner(first_card, second_card):
            first_deck.extend([first_card, second_card])
        else:
            second_deck.extend([first_card, second_card])

        if rounds >= max_rounds:
            return "botva"

    return "first" if first_deck else "second", rounds


def is_first_player_winner(card1: str, card2: str) -> bool:
    # Определяем победителя по правилам игры
    return (card1 > card2 and (card2, card1) != ('0', '9')) or (card1 == '0' and card2 == '9')


def main() -> None:
    # Ввод данных
    first_player_input = deque(input().split())
    second_player_input = deque(input().split())

    # Запуск игры
    result = play_game(first_player_input, second_player_input)

    # Вывод результата
    if result == "botva":
        print(result)
    else:
        winner, rounds = result
        print(winner, rounds)


if __name__ == '__main__':
    main()
