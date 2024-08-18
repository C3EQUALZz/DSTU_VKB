using System;
using System.Drawing;
using System.Linq;
using System.Windows.Forms;
using ThirdLaboratory.core;
using ThirdLaboratory.core.helpers;
using ThirdLaboratory.core.interfaces;
using ThirdLaboratory.presenters;

namespace ThirdLaboratory
{
    public partial class MainForm : Form, IMainView
    {
        private readonly MainPresenter _presenter;

        public MainForm()
        {
            InitializeComponent();
            this.SetBevel(false);

            _presenter = new MainPresenter(this, new FormFactory(this), new CommandContext(this), new SideBarContext(this));


            Controls.OfType<MdiClient>().FirstOrDefault().BackColor = Color.FromArgb(232, 234, 237);
        }

        public void Button_Click(object sender, EventArgs e)
        {
            _presenter.OnButtonClick(sender, e);
        }

        public void Timer_Tick(object sender, EventArgs e)
        {
            _presenter.OnTimerTick(sender, e);
        }

        public void TimerTransition_Tick(object sender, EventArgs e)
        {
            _presenter.OnTimerTransitionTick(sender, e);
        }

        public void MenuButton_Click(object sender, EventArgs e)
        {
            _presenter.OnMenuButtonClick(sender, e);
        }

        public void QuestionButton_Click(object sender, EventArgs e)
        {
            _presenter.OnQuestionButtonClick(sender, e);
        }

        public void UpdateSideBarWidth(int width)
        {
            sideBar.Width = width;
        }

        public void SetSideBarPanelsWidth(int width)
        {
            taskFlowPanel1To5.Width = width;
            taskFlowPanel6To10.Width = width;
            taskFlowPanel11To15.Width = width;
            taskFlowPanel16To20.Width = width;
        }

        public void ShowForm(Form form)
        {
            form.Show();
        }

        public void ActivateForm(Form form)
        {
            form.Activate();
        }

        public Form GetOpenFormByName(string formName)
        {
            return MdiChildren.FirstOrDefault(f => f.GetType().Name == formName);
        }


    }
}
