namespace ThirdLaboratory.core.interfaces.nineteenthQuestion
{
    internal interface INineteenthQuestionModel
    {
        int[,] Matrix { get; set; }
        int Rows { get; set; }
        int Columns { get; set; }

        void Initialize(int rows, int columns);
        void Execute(int numberOfColumn);
    }
}
