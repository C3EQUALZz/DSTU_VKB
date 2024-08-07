using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace ThirdLaboratory
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        bool menuExpand = false;

        private void TaskFlowPanel1To5_Tick(object sender, EventArgs e)
        {
            if (menuExpand == false)
            {
                taskFlowPanel1To5.Height += 10;

                if (taskFlowPanel1To5.Height >= 325)
                {
                    taskFlowPanel1To5Transition.Stop();
                    menuExpand = true;
                }
            }

            else
            {
                taskFlowPanel1To5.Height -= 10;

                if (taskFlowPanel1To5.Height <= 50)
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

        bool sideBarExpand = true;

        private void TimerTransition_Tick(object sender, EventArgs e)
        {
            if (sideBarExpand)
            {
                sideBar.Width -= 10;

                if (sideBar.Width <= 98)
                {
                    sideBarExpand = false;
                    sideBarTransition.Stop();
                }
            }

            else
            {
                sideBar.Width += 10;
                if (sideBar.Width >= 248)
                {
                    sideBarExpand = true;
                    sideBarTransition.Stop();

                }
            }
        }

        private void MenuButton_Click(object sender, EventArgs e)
        {
            sideBarTransition.Start();
        }
    }
}
