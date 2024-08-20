using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace ThirdLaboratory.core.interfaces.seventhQuestion
{
    internal interface ISeventhQuestionView
    {
        int RowCount { get; set; }
        int ColumnCount { get; set; }
        int[,] Matrix { get; set; }
        List<string> ResultListBoxItems { get; set; }
        void GenerateButton_Click(object sender, EventArgs e);
        void DataGridView_CellValidating(object sender, DataGridViewCellValidatingEventArgs e);
    }
}
