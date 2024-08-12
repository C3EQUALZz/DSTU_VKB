using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Windows.Forms;
using ThirdLaboratory.core;
using ThirdLaboratory.forms;

namespace ThirdLaboratory
{
    public partial class Form1 : Form
    {

        private readonly FormFactory _formFactory;

        public Form1()
        {
            InitializeComponent();
            this.SetBevel(false);

            _formFactory = new FormFactory(this);

            Controls.OfType<MdiClient>().FirstOrDefault().BackColor = Color.FromArgb(232, 234, 237);
        }

        bool firstToFifthQuestionExpand = false;
        bool sixthToTenthQuestionExpand = false;
        bool eleventhToFifteenthQuestionExpand = false;
        bool sixteenthToTwentiethQuestionExpand = false;

        bool sideBarExpand = true;

        private void TaskFlowPanel1To5_Tick(object sender, EventArgs e)
        {
            if (firstToFifthQuestionExpand == false)
            {
                taskFlowPanel1To5.Height += 10;

                if (taskFlowPanel1To5.Height >= 320)
                {
                    taskFlowPanel1To5Transition.Stop();
                    firstToFifthQuestionExpand = true;
                }
            }

            else
            {
                taskFlowPanel1To5.Height -= 10;

                if (taskFlowPanel1To5.Height <= 55)
                {
                    taskFlowPanel1To5Transition.Stop();
                    firstToFifthQuestionExpand = false;
                }
            }
        }

        private void FirstToFiveButton_Click(object sender, EventArgs e)
        {
            taskFlowPanel1To5Transition.Start();
        }

        

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
                    taskFlowPanel6to10.Width = sideBar.Width;
                    taskFlowPanel11to15.Width = sideBar.Width;
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
