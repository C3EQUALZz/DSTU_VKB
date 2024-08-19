using System;

namespace ThirdLaboratory.core.interfaces
{
    internal interface IMainPresenter
    {
        void OnMenuButtonClick(object sender, EventArgs e);
        void OnQuestionButtonClick(object sender, EventArgs e);
        void OnTimerTick(object sender, EventArgs e);
        void OnTimerTransitionTick(object sender, EventArgs e);
        void OnButtonClick(object sender, EventArgs e);
    }
}
