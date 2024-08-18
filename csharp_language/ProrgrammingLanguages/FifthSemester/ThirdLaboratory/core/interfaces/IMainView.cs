using System;

namespace ThirdLaboratory.core.interfaces
{
    internal interface IMainView
    {
        void MenuButton_Click(object sender, EventArgs e);
        void QuestionButton_Click(object sender, EventArgs e);
        void Timer_Tick(object sender, EventArgs e);
        void TimerTransition_Tick(object sender, EventArgs e);
        void Button_Click(object sender, EventArgs e);
    }
}
