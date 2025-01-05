"""
Задача №714. Турнир

В турнире по хоккею участвовало K команд, каждая сыграла с каждой по одному матчу. За победу команда получала 2 очка,
за ничью – 1, за поражение – 0 очков.

Известно, сколько очков в итоге получила каждая команда, однако результаты конкретных матчей были утеряны.
Требуется восстановить одну из возможных турнирных таблиц.

Входные данные

В первой строке входных данных содержится одно натурально число K, не превосходящее 100 – количество команд.
Во второй строке задаются через пробел K целых неотрицательных чисел, не превосходящих 2(K–1), – количество очков,
набранных командами, занявшими первое, второе, …, K-е места соответственно (то есть каждое следующее число не больше предыдущего).

Выходные данные

Выведите турнирную таблицу в следующем формате.
Таблица должна состоять из K строк с результатами игр команд, занявших первое, второе, …, последнее место
(команды, набравшие одинаковое число очков, могут быть расположены в таблице в любом порядке).
В каждой строке должно быть записано K чисел через пробел – количество очков, набранных в игре данной команды с первой,
второй, … командами соответственно. Количество очков – это число 0, 1 или 2.
В клетках на главной диагонали (соответствующих не существующей игре команды "самой с собой") нужно записать нули.

Гарантируется, что входные данные соответствуют реальному турниру, то есть хотя бы одна таблица,
соответствующая входным данным, может быть построена. Если таких таблиц несколько, выведите любую из них.
"""
from typing import List


def restore_tournament_table(num_teams: int, points: List[int]) -> List[List[int]]:
    # Инициализация таблицы результатов
    results = [[0] * num_teams for _ in range(num_teams)]

    # Индексы команд
    team_indices = list(range(num_teams))

    for i in range(num_teams - 1):
        # Сортируем команды по очкам
        sorted_points, sorted_indices = zip(*sorted(zip(points, team_indices)))
        sorted_points = list(sorted_points)
        sorted_indices = list(sorted_indices)

        for j in range(i + 1, num_teams):
            if results[sorted_indices[i]][sorted_indices[j]] > 0:
                continue
            elif sorted_points[i] > 0:
                # Ничья
                results[sorted_indices[i]][sorted_indices[j]] = 1
                results[sorted_indices[j]][sorted_indices[i]] = 1
                sorted_points[i] -= 1
                points[sorted_indices[j]] -= 1
            elif sorted_points[i] == 0:
                # Поражение
                results[sorted_indices[j]][sorted_indices[i]] = 2
                points[sorted_indices[j]] -= 2
        points[sorted_indices[i]] = -i - 1

    return results


def main():
    num_teams = int(input())
    points = list(map(int, input().split()))

    tournament_table = restore_tournament_table(num_teams, points)

    for row in tournament_table:
        print(*row)


if __name__ == "__main__":
    main()
