using System;
using System.Collections.Generic;
using System.Windows.Forms;

namespace ThirdLaboratory.Core.Interfaces.FifthQuestion
{
    internal interface IFifthQuestionView
    {
        int RowCount { get; set; }
        int ColumnCount { get; set; }
        string[,] Matrix { get; set; }
        List<string> ResultListBoxItems { get; set; }
        void ExecuteButton_Click(object sender, EventArgs e);
        void ClearButton_Click(object sender, EventArgs e);
        void DataGridView_CellValidating(object sender, DataGridViewCellValidatingEventArgs e);
    }
}
