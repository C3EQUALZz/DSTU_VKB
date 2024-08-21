using ThirdLaboratory.core.interfaces;

namespace ThirdLaboratory.models
{
    internal class NinthQuestionModel : INinthQuestionModel
    {
        public int[,] Matrix { get; set; }
        public int Rows { get; set; }
        public int Columns { get; set; }

        public void Initialize(int rows, int columns)
        {
            Rows = rows;
            Columns = columns;
            Matrix = new int[rows, columns];
        }

        public void SetCellValue(int row, int col, int value)
        {
            Matrix[row, col] = value;
        }

        public int GetCellValue(int row, int col)
        {
            return Matrix[row, col];
        }

        public bool IsColumnAllPositive(int colIndex)
        {
            for (int i = 0; i < Rows; i++)
            {
                if (Matrix[i, colIndex] <= 0)
                    return false;
            }
            return true;
        }

        public void SwapColumns(int col1, int col2)
        {
            for (int i = 0; i < Rows; i++)
            {
                (Matrix[i, col1], Matrix[i, col2]) = (Matrix[i, col2], Matrix[i, col1]);
            }
        }

        public void Execute()
        {
            for (int j = Columns - 2; j >= 0; j--)
            {
                if (IsColumnAllPositive(j))
                {
                    SwapColumns(j, Columns - 1);
                    break;
                }
            }
        }

    }
}
