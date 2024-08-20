using System;
using ThirdLaboratory.core.interfaces.seventhQuestion;

namespace ThirdLaboratory.models
{
    internal class SeventhQuestionModel : ISeventhQuestionModel
    {
        private readonly Random _random;
        private int[,] _matrix;

        /// <summary>
        /// Модель, которая отвечает за 7 вариант
        /// </summary>
        public SeventhQuestionModel()
        {
            _random = new Random();
        }

        /// <summary>
        /// Метод, который создает случайную матрицу по размерам, а также заполняет случайными элементами
        /// </summary>
        public int[,] Execute()
        {
            _matrix = new int[_random.Next(5, 10), _random.Next(5, 10)];

            var rows = _matrix.GetLength(0);
            var columns = _matrix.GetLength(1);

            for (var i = 0; i < rows; i++)
            {
                for (var j = 0; j < columns; j++)
                {
                    _matrix[i, j] = _random.Next(-100, 100);
                }
            }

            return _matrix;

        }

    }
}
