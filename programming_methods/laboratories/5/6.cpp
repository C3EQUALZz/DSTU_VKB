/* Венгерский алгоритм.
 * Реализация навеяна псевдокодом А.С.Лопатина из книги
 * "Оптимизация на графах (алгоритмы и реализация)".
 */

#include <vector>
#include <limits>
#include <iostream>

using namespace std;

typedef pair<int, int> PInt;
typedef vector<int> VInt;
typedef vector<VInt> VVInt;
typedef vector<PInt> VPInt;

const int inf = numeric_limits<int>::max();

/*
 * Решает задачу о назначениях Венгерским методом.
 * matrix: прямоугольная матрица из целых чисел (не обязательно положительных).
 *         Высота матрицы должна быть не больше ширины.
 * Возвращает: Список выбранных элементов, по одному из каждой строки матрицы.
 */
VPInt hungarian(const VVInt &matrix) {

	// Размеры матрицы
	int height = matrix.size(), width = matrix[0].size();

	// Значения, вычитаемые из строк (u) и столбцов (v)
	VInt u(height, 0), v(width, 0);

	// Индекс помеченной клетки в каждом столбце
	VInt markIndices(width, -1);

	// Будем добавлять строки матрицы одну за другой
	for(int i = 0; i < height; i++) {
		VInt links(width, -1);
		VInt mins(width, inf);
		VInt visited(width, 0);

		// Разрешение коллизий (создание "чередующейся цепочки" из нулевых элементов)
		int markedI = i, markedJ = -1, j;
		while(markedI != -1) {
			// Обновим информацию о минимумах в посещенных строках непосещенных столбцов
			// Заодно поместим в j индекс непосещенного столбца с самым маленьким из них
			j = -1;
			for(int j1 = 0; j1 < width; j1++)
				if(!visited[j1]) {
					if(matrix[markedI][j1] - u[markedI] - v[j1] < mins[j1]) {
						mins[j1] = matrix[markedI][j1] - u[markedI] - v[j1];
						links[j1] = markedJ;
					}
					if(j==-1 || mins[j1] < mins[j])
						j = j1;
				}

			// Теперь нас интересует элемент с индексами (markIndices[links[j]], j)
			// Произведем манипуляции со строками и столбцами так, чтобы он обнулился
			int delta = mins[j];
			for(int j1 = 0; j1 < width; j1++)
				if(visited[j1]) {
					u[markIndices[j1]] += delta;
					v[j1] -= delta;
				} else {
					mins[j1] -= delta;
				}
			u[i] += delta;

			// Если коллизия не разрешена - перейдем к следующей итерации
			visited[j] = 1;
			markedJ = j;
			markedI = markIndices[j];
		}

		// Пройдем по найденной чередующейся цепочке клеток, снимем отметки с
		// отмеченных клеток и поставим отметки на неотмеченные
		for(; links[j] != -1; j = links[j])
			markIndices[j] = markIndices[links[j]];
		markIndices[j] = i;
	}

	// Вернем результат в естественной форме
	VPInt result;
	for(int j = 0; j < width; j++)
		if(markIndices[j] != -1)
			result.push_back(PInt(markIndices[j], j));
	return result;
}


int main() {

	int k;
	VVInt a;
	int s=0;
	cin >> k;
	for(int i=0; i<k; ++i) {
		a.push_back(vector<int>(k));
	}

	for(int i=0; i<k; ++i) {
		for(int j=0; j<k; ++j) {
			cin >> a[i][j];
		}
	}

	VPInt r=hungarian(a);

	for(int i=0; i<k; ++i) {
		s+=a[r[i].first][r[i].second];
	}
	cout << s;

	return 0;
}


