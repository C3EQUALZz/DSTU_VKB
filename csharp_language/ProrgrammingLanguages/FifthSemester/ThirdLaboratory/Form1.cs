using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using ThirdLaboratory.core;
using ThirdLaboratory.forms;

namespace ThirdLaboratory
{
    public partial class Form1 : Form
    {
        FormFirstQuestion formFirstQuestion;
        FormSecondQuestion formSecondQuestion;
        FormThirdQuestion formThirdQuestion;
        FormFourthQuestion formFourthQuestion;
        FormFifthQuestion formFifthQuestion;
        FormSixthQuestion formSixthQuestion;
        FormSeventhQuestion formSeventhQuestion;
        FormEigthQuestion formEigthQuestion;
        FormNinthQuestion formNinthQuestion;
        FormTenthQuestion formTenthQuestion;
        FormEleventhQuestion formEleventhQuestion;
        FormTwelfthQuestion formTwelfthQuestion;
        FormThirteenthQuestion formThirteenthQuestion;
        FormFourteenthQuestion formFourteenthQuestion;
        FormFifteenthQuestion formFifteenthQuestion;
        FormSixteenthQuestion formSixteenthQuestion;
        FormSeventeenthQuestion formSeventeenthQuestion;
        FormEighteenthQuestion formEighteenthQuestion;
        FormNineteenthQuestion formNineteenthQuestion;
        FormTwentiethQuestion formTwentiethQuestion;

        private readonly FormFactory _formFactory;

        public Form1()
        {
            InitializeComponent();
            this.SetBevel(false);
            _formFactory = new FormFactory(this);
            Controls.OfType<MdiClient>().FirstOrDefault().BackColor = Color.FromArgb(232, 234, 237);
        }

        bool menuExpand = false;
        bool sideBarExpand = true;

        private void MdiProperty()
        {
            
        }

        private void TaskFlowPanel1To5_Tick(object sender, EventArgs e)
        {
            if (menuExpand == false)
            {
                taskFlowPanel1To5.Height += 10;

                if (taskFlowPanel1To5.Height >= 404)
                {
                    taskFlowPanel1To5Transition.Stop();
                    menuExpand = true;
                }
            }

            else
            {
                taskFlowPanel1To5.Height -= 10;

                if (taskFlowPanel1To5.Height <= 55)
                {
                    taskFlowPanel1To5Transition.Stop();
                    menuExpand = false;
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

        private void FirstQuestionButton_Click(object sender, EventArgs e) => ShowForm(ref formFirstQuestion);
        private void SecondQuestionButton_Click(object sender, EventArgs e) => ShowForm(ref formSecondQuestion);
        private void ThirdQuestionButton_Click(object sender, EventArgs e) => ShowForm(ref formThirdQuestion);
        private void FourthQuestionButton_Click(object sender, EventArgs e) => ShowForm(ref formFourthQuestion);
        private void FifthQuestionButton_Click(object sender, EventArgs e) => ShowForm(ref formFifthQuestion);
        private void SixthQuestionButton_Click(object sender, EventArgs e) => ShowForm(ref formSixthQuestion);
        private void SeventhQuestionButton_Click(object sender, EventArgs e) => ShowForm(ref formSeventhQuestion);
        private void EigthQuestionButton_Click(object sender, EventArgs e) => ShowForm(ref formEigthQuestion);
        private void NinthQuestionButton_Click(object sender, EventArgs e) => ShowForm(ref formNinthQuestion);
        private void TenthQuestionButton_Click(object sender, EventArgs e) => ShowForm(ref formTenthQuestion);
        private void EleventhQuestionButton_Click(object sender, EventArgs e) => ShowForm(ref formEleventhQuestion);
        private void TwelfthQuestionButton_Click(object sender, EventArgs e) => ShowForm(ref formTwelfthQuestion);
        private void ThirteenthQuestionButton_Click(object sender, EventArgs e) => ShowForm(ref formThirteenthQuestion);
        private void FourteenthQuestionButton_Click(object sender, EventArgs e) => ShowForm(ref formFourteenthQuestion);
        private void FifteenthQuestionButton_Click(object sender, EventArgs e) => ShowForm(ref formFifteenthQuestion);
        private void SixteenthQuestionButton_Click(object sender, EventArgs e) => ShowForm(ref formSixteenthQuestion);
        private void SeventeenthQuestionButton_Click(object sender, EventArgs e) => ShowForm(ref formSeventeenthQuestion);
        private void EigteenthQuestionButton_Click(object sender, EventArgs e) => ShowForm(ref formEighteenthQuestion);
        private void NineteenthQuestionButton_Click(object sender, EventArgs e) => ShowForm(ref formNineteenthQuestion);
        private void TwentiethQuestionButton_Click(object sender, EventArgs e) => ShowForm(ref formTwentiethQuestion);

        private void ShowForm<T>(ref T formInstance) where T : Form, new()
        {
            if (formInstance == null)
            {
                formInstance = _formFactory.Create<T>();
                formInstance.Show();
            }
            else
            {
                formInstance.Activate();
            }
        }
    }
}
