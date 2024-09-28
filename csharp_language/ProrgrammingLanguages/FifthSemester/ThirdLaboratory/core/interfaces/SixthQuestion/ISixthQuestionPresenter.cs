using System;

namespace ThirdLaboratory.Core.Interfaces.SixthQuestion
{
    internal interface ISixthQuestionPresenter
    {
        void OnStudentsTextBoxTextChanged(object sender, EventArgs e);
        void OnScholarShipTextBoxTextChanged(object sender, EventArgs e);
        void OnScholarShipRangeTextBoxTextChanged(object sender, EventArgs e);
        void OnExecute(object sender, EventArgs e);

    }
}
