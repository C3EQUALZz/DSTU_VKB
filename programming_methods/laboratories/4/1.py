"""
Задача №1889. Два коня

На стандартной шахматной доске (8×8) живут 2 шахматных коня: Красный и Зелёный.
Обычно они беззаботно скачут по просторам доски, пощипывая шахматную травку, но сегодня особенный день: у Зелёного коня день рождения.
Зелёный конь решил отпраздновать это событие вместе с Красным.
Но для осуществления этого прекрасного плана им нужно оказаться на одной клетке.
Заметим, что Красный и Зёленый шахматные кони сильно отличаются от черного с белым: они ходят не по очереди,
а одновременно, и, если оказываются на одной клетке, никто никого не съедает.
Сколько ходов им потребуется, чтобы насладиться праздником?

Входные данные

Во входном файле содержатся координаты коней, записанные по стандартным шахматным правилам
(т. е. двумя символами — маленькая латинская буква (от a до h) и цифра (от 1 до 8),
задающие столбец и строку соответственно).

Выходные данные

Выходной файл должен содержать наименьшее необходимое количество ходов, либо −1, если кони не могут встретиться.
"""
from collections import deque
from typing import Tuple, List


def get_moves(x: int, y: int) -> List[Tuple[int, int]]:
    moves = [
        (x + 1, y + 2), (x + 2, y + 1), (x + 2, y - 1), (x + 1, y - 2),
        (x - 1, y - 2), (x - 2, y - 1), (x - 2, y + 1), (x - 1, y + 2)
    ]
    return [(mx, my) for mx, my in moves if 0 <= mx <= 7 and 0 <= my <= 7]


def knights_meet(knight1: Tuple[int, int], knight2: Tuple[int, int]) -> int:
    visited = set()
    queue = deque([(knight1, knight2, 0)])

    while queue:
        k1, k2, moves = queue.popleft()

        if k1 == k2:
            return moves

        visited.add((k1, k2))

        k1_moves = get_moves(k1[0], k1[1])
        k2_moves = get_moves(k2[0], k2[1])

        for move1 in k1_moves:
            for move2 in k2_moves:
                if (move1, move2) not in visited:
                    visited.add((move1, move2))  # Добавляем в visited сразу
                    queue.append((move1, move2, moves + 1))

    return -1


def main() -> None:
    knight1, knight2 = input().split()
    knight1 = (ord(knight1[0]) - ord('a'), int(knight1[1]) - 1)
    knight2 = (ord(knight2[0]) - ord('a'), int(knight2[1]) - 1)

    result = knights_meet(knight1, knight2)
    print(result)


if __name__ == "__main__":
    main()
