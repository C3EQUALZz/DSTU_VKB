﻿using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace FirstLaboratory.ThirdQuestion
{
    public partial class SecondQuestionView : Form
    {
        private int openDocuments = 0;
        public SecondQuestionView()
        {
            InitializeComponent();
        }

        private void ExitMenuItem_Click(object sender, EventArgs e)
        {
            Close();
        }

        private void WindowCascadeMenuItem_Click(object sender, EventArgs e)
        {
            LayoutMdi(MdiLayout.Cascade);
        }

        private void WindowTileMenuItem_Click(object sender, EventArgs e)
        {
            LayoutMdi(MdiLayout.TileHorizontal);
        }

        private void NewMenuItem_Click(object sender, EventArgs e)
        {
            ChildForm newChild = new()
            {
                MdiParent = this
            };
            newChild.Text = newChild.Text + " " + ++openDocuments;

            newChild.Show();
        }
    }
}