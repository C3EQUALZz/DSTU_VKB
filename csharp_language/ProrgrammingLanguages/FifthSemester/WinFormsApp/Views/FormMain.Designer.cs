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
            iconButton6 = new FontAwesome.Sharp.IconButton();
            iconButton5 = new FontAwesome.Sharp.IconButton();
            iconButton4 = new FontAwesome.Sharp.IconButton();
            iconButton3 = new FontAwesome.Sharp.IconButton();
            iconButton2 = new FontAwesome.Sharp.IconButton();
            panelLogo = new Panel();
            MenuButton = new FontAwesome.Sharp.IconButton();
            LabelMenu = new Label();
            panelTitleBar = new Panel();
            label2 = new Label();
            MinimizeButton = new FontAwesome.Sharp.IconButton();
            CloseButton = new FontAwesome.Sharp.IconButton();
            MaximizeButton = new FontAwesome.Sharp.IconButton();
            panel1 = new Panel();
            iconSplitButton1 = new FontAwesome.Sharp.IconSplitButton();
            MenuPanel.SuspendLayout();
            panelLogo.SuspendLayout();
            panelTitleBar.SuspendLayout();
            SuspendLayout();
            // 
            // MenuPanel
            // 
            MenuPanel.BackColor = Color.FromArgb(51, 51, 76);
            MenuPanel.Controls.Add(iconButton6);
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
            // iconButton6
            // 
            iconButton6.AutoSize = true;
            iconButton6.Dock = DockStyle.Bottom;
            iconButton6.FlatAppearance.BorderSize = 0;
            iconButton6.FlatStyle = FlatStyle.Flat;
            iconButton6.Font = new Font("JetBrains Mono ExtraBold", 10F);
            iconButton6.ForeColor = Color.Gainsboro;
            iconButton6.IconChar = FontAwesome.Sharp.IconChar.SignOut;
            iconButton6.IconColor = Color.White;
            iconButton6.IconFont = FontAwesome.Sharp.IconFont.Auto;
            iconButton6.IconSize = 30;
            iconButton6.ImageAlign = ContentAlignment.MiddleLeft;
            iconButton6.Location = new Point(0, 453);
            iconButton6.Name = "iconButton6";
            iconButton6.Padding = new Padding(15, 0, 0, 15);
            iconButton6.Size = new Size(220, 51);
            iconButton6.TabIndex = 9;
            iconButton6.Tag = "Exit";
            iconButton6.Text = "  Выйти";
            iconButton6.TextImageRelation = TextImageRelation.ImageBeforeText;
            iconButton6.UseVisualStyleBackColor = true;
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
            iconButton5.Tag = "Лабораторная №4";
            iconButton5.Text = "  Лабораторная №4";
            iconButton5.TextImageRelation = TextImageRelation.ImageBeforeText;
            iconButton5.UseVisualStyleBackColor = true;
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
            iconButton4.Tag = "Лабораторная №3";
            iconButton4.Text = "  Лабораторная №3";
            iconButton4.TextImageRelation = TextImageRelation.ImageBeforeText;
            iconButton4.UseVisualStyleBackColor = true;
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
            iconButton3.Tag = "Лабораторная №2";
            iconButton3.Text = "  Лабораторная №2";
            iconButton3.TextImageRelation = TextImageRelation.ImageBeforeText;
            iconButton3.UseVisualStyleBackColor = true;
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
            iconButton2.Tag = "Лабораторная №1";
            iconButton2.Text = "  Лабораторная №1";
            iconButton2.TextImageRelation = TextImageRelation.ImageBeforeText;
            iconButton2.UseVisualStyleBackColor = true;
            // 
            // panelLogo
            // 
            panelLogo.BackColor = Color.FromArgb(39, 39, 58);
            panelLogo.Controls.Add(MenuButton);
            panelLogo.Controls.Add(LabelMenu);
            panelLogo.Dock = DockStyle.Top;
            panelLogo.Location = new Point(0, 0);
            panelLogo.Name = "panelLogo";
            panelLogo.Size = new Size(220, 80);
            panelLogo.TabIndex = 0;
            // 
            // MenuButton
            // 
            MenuButton.Dock = DockStyle.Right;
            MenuButton.FlatAppearance.BorderSize = 0;
            MenuButton.FlatStyle = FlatStyle.Flat;
            MenuButton.IconChar = FontAwesome.Sharp.IconChar.AlignJustify;
            MenuButton.IconColor = Color.White;
            MenuButton.IconFont = FontAwesome.Sharp.IconFont.Auto;
            MenuButton.IconSize = 30;
            MenuButton.Location = new Point(160, 0);
            MenuButton.Name = "MenuButton";
            MenuButton.Size = new Size(60, 80);
            MenuButton.TabIndex = 5;
            MenuButton.Tag = "Menu";
            MenuButton.UseVisualStyleBackColor = true;
            MenuButton.Click += MenuButton_Click;
            // 
            // LabelMenu
            // 
            LabelMenu.AutoSize = true;
            LabelMenu.Font = new Font("FiraCode Nerd Font Mono SemBd", 17.9999981F, FontStyle.Bold);
            LabelMenu.ForeColor = Color.Gainsboro;
            LabelMenu.Location = new Point(22, 23);
            LabelMenu.Name = "LabelMenu";
            LabelMenu.Size = new Size(73, 29);
            LabelMenu.TabIndex = 0;
            LabelMenu.Text = "Меню";
            // 
            // panelTitleBar
            // 
            panelTitleBar.BackColor = Color.FromArgb(51, 51, 76);
            panelTitleBar.Controls.Add(label2);
            panelTitleBar.Controls.Add(MinimizeButton);
            panelTitleBar.Controls.Add(CloseButton);
            panelTitleBar.Controls.Add(MaximizeButton);
            panelTitleBar.Dock = DockStyle.Top;
            panelTitleBar.Location = new Point(220, 0);
            panelTitleBar.Name = "panelTitleBar";
            panelTitleBar.Size = new Size(837, 60);
            panelTitleBar.TabIndex = 1;
            panelTitleBar.MouseDown += panelTitleBar_MouseDown;
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.FlatStyle = FlatStyle.Flat;
            label2.Font = new Font("JetBrains Mono ExtraBold", 15.999999F, FontStyle.Bold | FontStyle.Italic);
            label2.ForeColor = Color.Gainsboro;
            label2.Location = new Point(6, 22);
            label2.Name = "label2";
            label2.RightToLeft = RightToLeft.No;
            label2.Size = new Size(130, 29);
            label2.TabIndex = 11;
            label2.Text = "Dashboard";
            label2.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // MinimizeButton
            // 
            MinimizeButton.Anchor = AnchorStyles.Top | AnchorStyles.Right;
            MinimizeButton.BackColor = Color.DarkCyan;
            MinimizeButton.FlatAppearance.BorderSize = 0;
            MinimizeButton.FlatStyle = FlatStyle.Flat;
            MinimizeButton.IconChar = FontAwesome.Sharp.IconChar.AngleDown;
            MinimizeButton.IconColor = Color.White;
            MinimizeButton.IconFont = FontAwesome.Sharp.IconFont.Auto;
            MinimizeButton.IconSize = 20;
            MinimizeButton.Location = new Point(702, 0);
            MinimizeButton.Name = "MinimizeButton";
            MinimizeButton.Padding = new Padding(0, 15, 0, 10);
            MinimizeButton.Size = new Size(45, 25);
            MinimizeButton.TabIndex = 10;
            MinimizeButton.UseVisualStyleBackColor = false;
            MinimizeButton.Click += MinimizeButton_Click;
            // 
            // CloseButton
            // 
            CloseButton.Anchor = AnchorStyles.Top | AnchorStyles.Right;
            CloseButton.BackColor = Color.FromArgb(254, 74, 130);
            CloseButton.FlatAppearance.BorderSize = 0;
            CloseButton.FlatStyle = FlatStyle.Flat;
            CloseButton.IconChar = FontAwesome.Sharp.IconChar.TimesSquare;
            CloseButton.IconColor = Color.White;
            CloseButton.IconFont = FontAwesome.Sharp.IconFont.Auto;
            CloseButton.IconSize = 20;
            CloseButton.Location = new Point(792, 0);
            CloseButton.Name = "CloseButton";
            CloseButton.Size = new Size(45, 25);
            CloseButton.TabIndex = 9;
            CloseButton.UseVisualStyleBackColor = false;
            CloseButton.Click += CloseButton_Click;
            // 
            // MaximizeButton
            // 
            MaximizeButton.Anchor = AnchorStyles.Top | AnchorStyles.Right;
            MaximizeButton.BackColor = Color.RoyalBlue;
            MaximizeButton.FlatAppearance.BorderSize = 0;
            MaximizeButton.FlatStyle = FlatStyle.Flat;
            MaximizeButton.IconChar = FontAwesome.Sharp.IconChar.Square;
            MaximizeButton.IconColor = Color.White;
            MaximizeButton.IconFont = FontAwesome.Sharp.IconFont.Auto;
            MaximizeButton.IconSize = 20;
            MaximizeButton.Location = new Point(747, 0);
            MaximizeButton.Name = "MaximizeButton";
            MaximizeButton.Size = new Size(45, 25);
            MaximizeButton.TabIndex = 6;
            MaximizeButton.UseVisualStyleBackColor = false;
            MaximizeButton.Click += MaximizeButton_Click;
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
            // iconSplitButton1
            // 
            iconSplitButton1.Flip = FontAwesome.Sharp.FlipOrientation.Normal;
            iconSplitButton1.IconChar = FontAwesome.Sharp.IconChar.None;
            iconSplitButton1.IconColor = Color.Black;
            iconSplitButton1.IconFont = FontAwesome.Sharp.IconFont.Auto;
            iconSplitButton1.IconSize = 48;
            iconSplitButton1.Name = "iconSplitButton1";
            iconSplitButton1.Rotation = 0D;
            iconSplitButton1.Size = new Size(23, 23);
            iconSplitButton1.Text = "iconSplitButton1";
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
            StartPosition = FormStartPosition.CenterScreen;
            Text = "Ковалев Данил ВКБ22";
            Resize += FormResizeEvent;
            MenuPanel.ResumeLayout(false);
            MenuPanel.PerformLayout();
            panelLogo.ResumeLayout(false);
            panelLogo.PerformLayout();
            panelTitleBar.ResumeLayout(false);
            panelTitleBar.PerformLayout();
            ResumeLayout(false);
        }

        #endregion

        private Panel MenuPanel;
        private Panel panel1;
        private Panel panelLogo;
        private Label LabelMenu;
        private FontAwesome.Sharp.IconButton MenuButton;
        private FontAwesome.Sharp.IconButton iconButton2;
        private FontAwesome.Sharp.IconButton iconButton5;
        private FontAwesome.Sharp.IconButton iconButton4;
        private FontAwesome.Sharp.IconButton iconButton3;
        private FontAwesome.Sharp.IconSplitButton iconSplitButton1;
        private FontAwesome.Sharp.IconButton iconButton6;
        private FontAwesome.Sharp.IconButton MaximizeButton;
        private FontAwesome.Sharp.IconButton CloseButton;
        private FontAwesome.Sharp.IconButton MinimizeButton;
        private Label label2;
        private Panel panelTitleBar;
    }
}