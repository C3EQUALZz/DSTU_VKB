using System;
using System.Linq;
using ThirdLaboratory.core.interfaces.nineteenthQuestion;

namespace ThirdLaboratory.models
{
    internal class NineteenthQuestionModel : INineteenthQuestionModel
    {
        public int[,] Matrix { get; set; }
        public int Rows { get; set; }
        public int Columns { get; set; }

        /// <summary>
        /// Делаю инициализацию матрциы здесь, через конструктор класса нельзя, так как он раньше отработает, чем все ивенты
        /// </summary>
        /// <param name="rows">количество строк для матрицы</param>
        /// <param name="columns">количество столбцов для матрицы</param>
        public void Initialize(int rows, int columns)
        {
            Rows = rows;
            Columns = columns;
            Matrix = CreateRandomMatrix(rows, columns);
        }

        /// <summary>
        /// Метод для удаления столбца матрицы
        /// </summary>
        /// <param name="columnIndex">номер, который ввел пользователь для удаления</param>
        public void Execute(int columnIndex)
        {
            columnIndex -= 1;

            var newMatrix = new int[Rows, Columns - 1];

            for (var i = 0; i < Rows; i++)
            {
                var newColumnIndex = 0;

                for (var j = 0; j < Columns; j++)
                {
                    if (j == columnIndex)
                        continue; 

                    newMatrix[i, newColumnIndex] = Matrix[i, j];
                    newColumnIndex++;
                }
            }

            Matrix = newMatrix;
            Columns--;
        }

        /// <summary>
        /// Приватный метод для создания матрицы, содержащей случайные значения
        /// </summary>
        /// <param name="rows">количество строк</param>
        /// <param name="columns">количество колонок</param>
        /// <returns>возвращает полностью заполенную матрицу</returns>
        private int[,] CreateRandomMatrix(int rows, int columns)
        {
            var random = new Random();

            var matrix = new int[rows, columns];

            Enumerable.Range(0, rows).ToList().ForEach(i =>
            {
                Enumerable.Range(0, columns).ToList().ForEach(j =>
                {
                    matrix[i, j] = random.Next(1, 100);
                });
            });

            return matrix;
        }
    }
}
