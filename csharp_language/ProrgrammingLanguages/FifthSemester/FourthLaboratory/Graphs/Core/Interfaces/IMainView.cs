using System;
using System.Windows.Forms;

namespace DoAnPaint.Graphs.Core.Interfaces
{
    internal interface IMainView
    {
        void ShowForm(Form form);
        void ActivateForm(Form form);
        Form GetOpenFormByName(string formName);
        void QuestionButton_Click(object sender, EventArgs e);
    }
}
