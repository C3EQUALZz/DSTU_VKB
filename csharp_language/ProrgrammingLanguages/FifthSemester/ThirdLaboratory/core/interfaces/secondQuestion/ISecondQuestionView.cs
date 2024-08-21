using System;

namespace ThirdLaboratory.core.interfaces
{
    internal interface ISecondQuestionView : IQuestionForm
    {
        string StaffInput { get; set; }
        string RequestsInput { get; set; }
        string ResultOutput { get; set; }

        void StaffInput__TextChanged(object sender, EventArgs e);
        void RequestsInput__TextChanged(object sender, EventArgs e);
    }
}
