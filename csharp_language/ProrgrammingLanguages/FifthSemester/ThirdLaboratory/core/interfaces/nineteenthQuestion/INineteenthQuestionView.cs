using System;

namespace ThirdLaboratory.core.interfaces.nineteenthQuestion
{
    internal interface INineteenthQuestionView : IQuestionForm
    {
        int RowCount { get; set; }
        int ColumnCount { get; set; }
        int[,] Matrix { get; set; }
        string[] RowHeaders { get; set; }
        string[] ColumnHeaders { get; set; }
        void CreateMatrixButton_Click(object sender, EventArgs e);

    }
}
