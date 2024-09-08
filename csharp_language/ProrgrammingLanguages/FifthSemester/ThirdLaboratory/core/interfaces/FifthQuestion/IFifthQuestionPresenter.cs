using System;
using System.Windows.Forms;

namespace ThirdLaboratory.Core.Interfaces.FifthQuestion
{
    internal interface IFifthQuestionPresenter
    {
        void OnExecute(object sender, EventArgs e);
        void OnCellValidate(object sender, DataGridViewCellValidatingEventArgs e);
    }
}
