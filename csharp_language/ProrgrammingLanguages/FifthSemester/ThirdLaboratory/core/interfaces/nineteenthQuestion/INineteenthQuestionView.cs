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
        void NumberOfDeletingColumn__TextChanged(object sender, EventArgs e);
        void CountOfColumnsInput__TextChanged(object sender, EventArgs e);
        void CountOfRowsInput__TextChanged(object sender, EventArgs e);
    }
}
