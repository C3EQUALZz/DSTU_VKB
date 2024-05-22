namespace WinFormsApp.Views
{
    partial class FormMain
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            MenuPanel = new Panel();
            panelLogo = new Panel();
            label1 = new Label();
            panelTitleBar = new Panel();
            panel1 = new Panel();
            iconButton1 = new FontAwesome.Sharp.IconButton();
            iconButton2 = new FontAwesome.Sharp.IconButton();
            iconButton3 = new FontAwesome.Sharp.IconButton();
            iconButton4 = new FontAwesome.Sharp.IconButton();
            iconButton5 = new FontAwesome.Sharp.IconButton();
            MenuPanel.SuspendLayout();
            panelLogo.SuspendLayout();
            SuspendLayout();
            // 
            // MenuPanel
            // 
            MenuPanel.BackColor = Color.FromArgb(51, 51, 76);
            MenuPanel.Controls.Add(iconButton5);
            MenuPanel.Controls.Add(iconButton4);
            MenuPanel.Controls.Add(iconButton3);
            MenuPanel.Controls.Add(iconButton2);
            MenuPanel.Controls.Add(panelLogo);
            MenuPanel.Dock = DockStyle.Left;
            MenuPanel.Location = new Point(0, 0);
            MenuPanel.Name = "MenuPanel";
            MenuPanel.Size = new Size(220, 504);
            MenuPanel.TabIndex = 0;
            // 
            // panelLogo
            // 
            panelLogo.BackColor = Color.FromArgb(39, 39, 58);
            panelLogo.Controls.Add(iconButton1);
            panelLogo.Controls.Add(label1);
            panelLogo.Dock = DockStyle.Top;
            panelLogo.Location = new Point(0, 0);
            panelLogo.Name = "panelLogo";
            panelLogo.Size = new Size(220, 80);
            panelLogo.TabIndex = 0;
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Font = new Font("FiraCode Nerd Font Mono SemBd", 17.9999981F, FontStyle.Bold);
            label1.ForeColor = Color.Gainsboro;
            label1.Location = new Point(22, 23);
            label1.Name = "label1";
            label1.Size = new Size(73, 29);
            label1.TabIndex = 0;
            label1.Text = "Меню";
            label1.Click += label1_Click;
            // 
            // panelTitleBar
            // 
            panelTitleBar.Dock = DockStyle.Top;
            panelTitleBar.Location = new Point(220, 0);
            panelTitleBar.Name = "panelTitleBar";
            panelTitleBar.Size = new Size(837, 60);
            panelTitleBar.TabIndex = 1;
            // 
            // panel1
            // 
            panel1.BackColor = Color.FromArgb(245, 245, 254);
            panel1.Dock = DockStyle.Fill;
            panel1.Location = new Point(220, 60);
            panel1.Name = "panel1";
            panel1.Size = new Size(837, 444);
            panel1.TabIndex = 2;
            // 
            // iconButton1
            // 
            iconButton1.Dock = DockStyle.Right;
            iconButton1.FlatAppearance.BorderSize = 0;
            iconButton1.FlatStyle = FlatStyle.Flat;
            iconButton1.IconChar = FontAwesome.Sharp.IconChar.AlignJustify;
            iconButton1.IconColor = Color.White;
            iconButton1.IconFont = FontAwesome.Sharp.IconFont.Auto;
            iconButton1.IconSize = 30;
            iconButton1.Location = new Point(160, 0);
            iconButton1.Name = "iconButton1";
            iconButton1.Size = new Size(60, 80);
            iconButton1.TabIndex = 5;
            iconButton1.UseVisualStyleBackColor = true;
            // 
            // iconButton2
            // 
            iconButton2.AutoSize = true;
            iconButton2.Dock = DockStyle.Top;
            iconButton2.FlatAppearance.BorderSize = 0;
            iconButton2.FlatStyle = FlatStyle.Flat;
            iconButton2.Font = new Font("JetBrains Mono ExtraBold", 10F);
            iconButton2.ForeColor = Color.Gainsboro;
            iconButton2.IconChar = FontAwesome.Sharp.IconChar.GripHorizontal;
            iconButton2.IconColor = Color.White;
            iconButton2.IconFont = FontAwesome.Sharp.IconFont.Auto;
            iconButton2.IconSize = 30;
            iconButton2.ImageAlign = ContentAlignment.MiddleLeft;
            iconButton2.Location = new Point(0, 80);
            iconButton2.Name = "iconButton2";
            iconButton2.Padding = new Padding(15, 0, 0, 0);
            iconButton2.Size = new Size(220, 49);
            iconButton2.TabIndex = 5;
            iconButton2.Text = "  Лабораторная №1";
            iconButton2.TextImageRelation = TextImageRelation.ImageBeforeText;
            iconButton2.UseVisualStyleBackColor = true;
            // 
            // iconButton3
            // 
            iconButton3.AutoSize = true;
            iconButton3.Dock = DockStyle.Top;
            iconButton3.FlatAppearance.BorderSize = 0;
            iconButton3.FlatStyle = FlatStyle.Flat;
            iconButton3.Font = new Font("JetBrains Mono ExtraBold", 10F);
            iconButton3.ForeColor = Color.Gainsboro;
            iconButton3.IconChar = FontAwesome.Sharp.IconChar.GripHorizontal;
            iconButton3.IconColor = Color.White;
            iconButton3.IconFont = FontAwesome.Sharp.IconFont.Auto;
            iconButton3.IconSize = 30;
            iconButton3.ImageAlign = ContentAlignment.MiddleLeft;
            iconButton3.Location = new Point(0, 129);
            iconButton3.Name = "iconButton3";
            iconButton3.Padding = new Padding(15, 0, 0, 0);
            iconButton3.Size = new Size(220, 49);
            iconButton3.TabIndex = 6;
            iconButton3.Text = "  Лабораторная №2";
            iconButton3.TextImageRelation = TextImageRelation.ImageBeforeText;
            iconButton3.UseVisualStyleBackColor = true;
            // 
            // iconButton4
            // 
            iconButton4.AutoSize = true;
            iconButton4.Dock = DockStyle.Top;
            iconButton4.FlatAppearance.BorderSize = 0;
            iconButton4.FlatStyle = FlatStyle.Flat;
            iconButton4.Font = new Font("JetBrains Mono ExtraBold", 10F);
            iconButton4.ForeColor = Color.Gainsboro;
            iconButton4.IconChar = FontAwesome.Sharp.IconChar.GripHorizontal;
            iconButton4.IconColor = Color.White;
            iconButton4.IconFont = FontAwesome.Sharp.IconFont.Auto;
            iconButton4.IconSize = 30;
            iconButton4.ImageAlign = ContentAlignment.MiddleLeft;
            iconButton4.Location = new Point(0, 178);
            iconButton4.Name = "iconButton4";
            iconButton4.Padding = new Padding(15, 0, 0, 0);
            iconButton4.Size = new Size(220, 49);
            iconButton4.TabIndex = 7;
            iconButton4.Text = "  Лабораторная №3";
            iconButton4.TextImageRelation = TextImageRelation.ImageBeforeText;
            iconButton4.UseVisualStyleBackColor = true;
            // 
            // iconButton5
            // 
            iconButton5.AutoSize = true;
            iconButton5.Dock = DockStyle.Top;
            iconButton5.FlatAppearance.BorderSize = 0;
            iconButton5.FlatStyle = FlatStyle.Flat;
            iconButton5.Font = new Font("JetBrains Mono ExtraBold", 10F);
            iconButton5.ForeColor = Color.Gainsboro;
            iconButton5.IconChar = FontAwesome.Sharp.IconChar.GripHorizontal;
            iconButton5.IconColor = Color.White;
            iconButton5.IconFont = FontAwesome.Sharp.IconFont.Auto;
            iconButton5.IconSize = 30;
            iconButton5.ImageAlign = ContentAlignment.MiddleLeft;
            iconButton5.Location = new Point(0, 227);
            iconButton5.Name = "iconButton5";
            iconButton5.Padding = new Padding(15, 0, 0, 0);
            iconButton5.Size = new Size(220, 49);
            iconButton5.TabIndex = 8;
            iconButton5.Text = "  Лабораторная №4";
            iconButton5.TextImageRelation = TextImageRelation.ImageBeforeText;
            iconButton5.UseVisualStyleBackColor = true;
            // 
            // FormMain
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(1057, 504);
            Controls.Add(panel1);
            Controls.Add(panelTitleBar);
            Controls.Add(MenuPanel);
            Font = new Font("FiraCode Nerd Font Mono SemBd", 8.999999F, FontStyle.Bold, GraphicsUnit.Point, 0);
            Name = "FormMain";
            Text = "Ковалев Данил ВКБ22";
            MenuPanel.ResumeLayout(false);
            MenuPanel.PerformLayout();
            panelLogo.ResumeLayout(false);
            panelLogo.PerformLayout();
            ResumeLayout(false);
        }

        #endregion

        private Panel MenuPanel;
        private Panel panelTitleBar;
        private Panel panel1;
        private Panel panelLogo;
        private Label label1;
        private FontAwesome.Sharp.IconButton iconButton1;
        private FontAwesome.Sharp.IconButton iconButton2;
        private FontAwesome.Sharp.IconButton iconButton5;
        private FontAwesome.Sharp.IconButton iconButton4;
        private FontAwesome.Sharp.IconButton iconButton3;
    }
}