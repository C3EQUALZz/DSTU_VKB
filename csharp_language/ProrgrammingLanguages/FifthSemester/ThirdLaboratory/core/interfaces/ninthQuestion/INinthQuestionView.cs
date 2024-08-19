using System;

namespace ThirdLaboratory.core.interfaces
{
    internal interface INinthQuestionView
    {
        int RowCount { get; set; }
        int ColumnCount { get; set; }
        int[,] Matrix { get; set; }
        string[] RowHeaders { get; set; }
        string[] ColumnHeaders { get; set; }

        void CountOfMatrixRowsTextBox__TextChanged(object sender, EventArgs e);
        void CountOfMatrixColumnsTextBox__TextChanged(object sender, EventArgs e);
        void CreateMatrixButton_Click(object sender, EventArgs e);

    }
}
