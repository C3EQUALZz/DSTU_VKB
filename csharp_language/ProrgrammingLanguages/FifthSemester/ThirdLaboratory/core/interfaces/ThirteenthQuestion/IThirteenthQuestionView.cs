using System;
using System.ComponentModel;

namespace ThirdLaboratory.Core.Interfaces.ThirteenthQuestion
{
    internal interface IThirteenthQuestionView
    {
        string[] RowHeaders { get; set; }
        string[] ColumnHeaders { get; set; }
        int RowCount { get; set; }
        int ColumnCount { get; set; }
        int[,] Matrix { get; set; }
        string OutputText { get; set; }
        void CountOfRows_Validating(object sender, CancelEventArgs e);
        void CountOfColumns_Validating(object sender, CancelEventArgs e);
        void NumberOfRow_Validating(object sender, CancelEventArgs e);
        void GenerateRandomMatrixButton_Click(object sender, EventArgs e);
        void ClearButton_Click(object sender, EventArgs e);
        void ExecuteButton_Click(object sender, EventArgs e);
    }
}
