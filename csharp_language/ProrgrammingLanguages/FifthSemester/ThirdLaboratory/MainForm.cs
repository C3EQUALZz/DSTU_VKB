using System;
using System.Drawing;
using System.Linq;
using System.Windows.Forms;
using ThirdLaboratory.core;
using ThirdLaboratory.core.helpers;

namespace ThirdLaboratory
{
    public partial class MainForm : Form
    {
        private readonly FormFactory _formFactory;
        private readonly CommandContext _commandContext;

        public MainForm()
        {
            InitializeComponent();
            this.SetBevel(false);

            _formFactory = new FormFactory(this);
            _commandContext = new CommandContext(this);

            Controls.OfType<MdiClient>().FirstOrDefault().BackColor = Color.FromArgb(232, 234, 237);
        }

        private void Button_Click(object sender, EventArgs e)
        {
            var button = sender as Button;
            string panelTag = button.Tag.ToString();
            _commandContext.SetCommand(panelTag);
        }

        private void Timer_Tick(object sender, EventArgs e)
        {
            _commandContext.Execute();
        }


        bool sideBarExpand = true;
        private void TimerTransition_Tick(object sender, EventArgs e)
        {
            if (sideBarExpand)
            {
                sideBar.Width -= 10;

                if (sideBar.Width <= 110)
                {
                    sideBarExpand = false;
                    sideBarTransition.Stop();

                }
            }

            else
            {
                sideBar.Width += 10;
                if (sideBar.Width >= 323)
                {
                    sideBarExpand = true;
                    sideBarTransition.Stop();

                    taskFlowPanel1To5.Width = sideBar.Width;
                    taskFlowPanel6To10.Width = sideBar.Width;
                    taskFlowPanel11To15.Width = sideBar.Width;
                    taskFlowPanel16To20.Width = sideBar.Width;
                }
            }
        }

        private void MenuButton_Click(object sender, EventArgs e)
        {
            sideBarTransition.Start();
        }

        private void QuestionButton_Click(object sender, EventArgs e)
        {
            if (sender is Button button && button.Tag is string formName)
            {
                // Ищем уже открытые формы с таким же именем
                Form formInstance = MdiChildren.FirstOrDefault(f => f.GetType().Name == formName);

                if (formInstance == null)
                {
                    // Используем фабрику для создания новой формы
                    formInstance = _formFactory.Create(formName);
                    formInstance.Show();
                }
                else
                {
                    formInstance.Activate();
                }
            }
        }

        
    }
}
