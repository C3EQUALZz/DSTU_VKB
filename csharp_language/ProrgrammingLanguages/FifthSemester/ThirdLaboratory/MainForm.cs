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
        private readonly SideBarContext _sideBarContext;

        public MainForm()
        {
            InitializeComponent();
            this.SetBevel(false);

            _formFactory = new FormFactory(this);
            _commandContext = new CommandContext(this);
            _sideBarContext = new SideBarContext(
                sideBar, 
                sideBarTransition,
                taskFlowPanel1To5,
                taskFlowPanel6To10,
                taskFlowPanel11To15,
                taskFlowPanel16To20
             );

            Controls.OfType<MdiClient>().FirstOrDefault().BackColor = Color.FromArgb(232, 234, 237);
        }

        private void Button_Click(object sender, EventArgs e)
        {
            var button = sender as Button;
            var panelTag = button.Tag.ToString();
            _commandContext.SetCommand(panelTag);
        }

        private void Timer_Tick(object sender, EventArgs e)
        {
            _commandContext.Execute();
        }

        private void TimerTransition_Tick(object sender, EventArgs e)
        {
            _sideBarContext.Handle();
        }

        private void MenuButton_Click(object sender, EventArgs e)
        {
            _sideBarContext.StartAnimation();
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
