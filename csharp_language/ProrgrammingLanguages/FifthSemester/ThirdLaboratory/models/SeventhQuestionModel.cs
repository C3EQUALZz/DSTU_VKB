using System;
using ThirdLaboratory.core.interfaces.seventhQuestion;

namespace ThirdLaboratory.models
{
    internal class SeventhQuestionModel : ISeventhQuestionModel
    {
        private readonly Random _random;
        public int[,] _matrix;

        public SeventhQuestionModel()
        {
            _random = new Random();
            _matrix = new int[6, 6];
        }

        public int[,] Execute()
        {
            int rows = _matrix.GetLength(0);
            int columns = _matrix.GetLength(1);

            for (int i = 0; i < rows; i++)
            {
                for (int j = 0; j < columns; j++)
                {
                    _matrix[i, j] = _random.Next(_random.Next(), _random.Next());
                }
            }

            return _matrix;

        }

    }
}
