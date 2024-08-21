namespace ThirdLaboratory.core.interfaces
{
    internal interface INinthQuestionModel
    {
        int[,] Matrix { get; set; }
        int Rows { get;  set; }
        int Columns { get; set; }

        void Initialize(int rows, int columns);
        void SetCellValue(int row, int col, int value);
        int GetCellValue(int row, int col);
        bool IsColumnAllPositive(int colIndex);
        void SwapColumns(int col1, int col2);
        void Execute();
    }
}
