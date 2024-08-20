using System;
using ThirdLaboratory.core.interfaces.seventhQuestion;

namespace ThirdLaboratory.models
{
    internal class SeventhQuestionModel : ISeventhQuestionModel
    {
        private readonly Random _random;
        private int[,] _matrix;

        public SeventhQuestionModel()
        {
            _random = new Random();
        }

        public int[,] Execute()
        {
            _matrix = new int[_random.Next(5, 10), _random.Next(5, 10)];

            int rows = _matrix.GetLength(0);
            int columns = _matrix.GetLength(1);

            for (int i = 0; i < rows; i++)
            {
                for (int j = 0; j < columns; j++)
                {
                    _matrix[i, j] = _random.Next(-100, 100);
                }
            }

            return _matrix;

        }

    }
}
