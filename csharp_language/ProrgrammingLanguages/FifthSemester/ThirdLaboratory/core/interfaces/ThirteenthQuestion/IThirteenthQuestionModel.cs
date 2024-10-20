namespace ThirdLaboratory.Core.Interfaces.ThirteenthQuestion
{
    internal interface IThirteenthQuestionModel
    {
        int[,] Matrix { get; set; }
        int Rows { get; set; }
        int Columns { get; set; }

        void Initialize(int rows, int columns);
        int[] Execute(int rowIndex);
    }
}
