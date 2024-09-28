using System;

namespace ThirdLaboratory.Core.Interfaces.SixthQuestion
{
    internal interface ISixthQuestionView
    {
        string StudentsTextBox { get; set; }
        string ScholarShipTextBox {  get; set; }
        string ScholarShipRangeTextBox { get; set; }
        string ResultLabel { get; set; }
        void StudentsTextBox__TextChanged(object sender, System.ComponentModel.CancelEventArgs e);
        void ScholarShipTextBox__TextChanged(object sender, System.ComponentModel.CancelEventArgs e);
        void ScholarShipRangeTextBox__TextChanged(object sender, System.ComponentModel.CancelEventArgs e);
        void ClearButton_Click(object sender, EventArgs e);
        void ExecuteButton_Click(object sender, EventArgs e);

    }
}
