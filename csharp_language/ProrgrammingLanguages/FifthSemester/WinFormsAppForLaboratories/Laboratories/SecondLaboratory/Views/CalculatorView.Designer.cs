namespace WinFormsAppForLaboratories.Laboratories.SecondLaboratory.Views
{
    partial class CalculatorView
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
            panelTitle = new Panel();
            panelHistory = new Panel();
            buttonExit = new FontAwesome.Sharp.IconButton();
            iconButton1 = new FontAwesome.Sharp.IconButton();
            iconButton2 = new FontAwesome.Sharp.IconButton();
            panel1 = new Panel();
            menuButton = new FontAwesome.Sharp.IconButton();
            buttonHistory = new FontAwesome.Sharp.IconButton();
            textDisplay2 = new TextBox();
            textDisplay1 = new TextBox();
            richTextBox1 = new RichTextBox();
            panelTitle.SuspendLayout();
            panelHistory.SuspendLayout();
            panel1.SuspendLayout();
            SuspendLayout();
            // 
            // panelTitle
            // 
            panelTitle.Controls.Add(iconButton2);
            panelTitle.Controls.Add(iconButton1);
            panelTitle.Controls.Add(buttonExit);
            panelTitle.Dock = DockStyle.Top;
            panelTitle.Location = new Point(0, 0);
            panelTitle.Margin = new Padding(0);
            panelTitle.Name = "panelTitle";
            panelTitle.Size = new Size(350, 40);
            panelTitle.TabIndex = 0;
            // 
            // panelHistory
            // 
            panelHistory.Controls.Add(richTextBox1);
            panelHistory.Dock = DockStyle.Bottom;
            panelHistory.Location = new Point(0, 530);
            panelHistory.Margin = new Padding(0);
            panelHistory.Name = "panelHistory";
            panelHistory.Size = new Size(350, 40);
            panelHistory.TabIndex = 1;
            // 
            // buttonExit
            // 
            buttonExit.Dock = DockStyle.Right;
            buttonExit.FlatAppearance.BorderSize = 0;
            buttonExit.FlatAppearance.MouseOverBackColor = Color.Red;
            buttonExit.FlatStyle = FlatStyle.Flat;
            buttonExit.ForeColor = Color.Transparent;
            buttonExit.IconChar = FontAwesome.Sharp.IconChar.Multiply;
            buttonExit.IconColor = Color.White;
            buttonExit.IconFont = FontAwesome.Sharp.IconFont.Auto;
            buttonExit.IconSize = 16;
            buttonExit.Location = new Point(300, 0);
            buttonExit.Margin = new Padding(0);
            buttonExit.Name = "buttonExit";
            buttonExit.Size = new Size(50, 40);
            buttonExit.TabIndex = 2;
            buttonExit.UseVisualStyleBackColor = true;
            // 
            // iconButton1
            // 
            iconButton1.Dock = DockStyle.Right;
            iconButton1.FlatAppearance.BorderSize = 0;
            iconButton1.FlatAppearance.MouseOverBackColor = Color.Red;
            iconButton1.FlatStyle = FlatStyle.Flat;
            iconButton1.ForeColor = Color.Transparent;
            iconButton1.IconChar = FontAwesome.Sharp.IconChar.SquareFull;
            iconButton1.IconColor = Color.White;
            iconButton1.IconFont = FontAwesome.Sharp.IconFont.Auto;
            iconButton1.IconSize = 15;
            iconButton1.Location = new Point(250, 0);
            iconButton1.Margin = new Padding(0);
            iconButton1.Name = "iconButton1";
            iconButton1.Size = new Size(50, 40);
            iconButton1.TabIndex = 3;
            iconButton1.UseVisualStyleBackColor = true;
            // 
            // iconButton2
            // 
            iconButton2.Dock = DockStyle.Right;
            iconButton2.FlatAppearance.BorderSize = 0;
            iconButton2.FlatAppearance.MouseOverBackColor = Color.Red;
            iconButton2.FlatStyle = FlatStyle.Flat;
            iconButton2.Font = new Font("Gadugi", 12F, FontStyle.Regular, GraphicsUnit.Point, 0);
            iconButton2.ForeColor = Color.Transparent;
            iconButton2.IconChar = FontAwesome.Sharp.IconChar.Minus;
            iconButton2.IconColor = Color.White;
            iconButton2.IconFont = FontAwesome.Sharp.IconFont.Auto;
            iconButton2.IconSize = 17;
            iconButton2.Location = new Point(200, 0);
            iconButton2.Margin = new Padding(0);
            iconButton2.Name = "iconButton2";
            iconButton2.Size = new Size(50, 40);
            iconButton2.TabIndex = 4;
            iconButton2.UseVisualStyleBackColor = true;
            // 
            // panel1
            // 
            panel1.Controls.Add(menuButton);
            panel1.Controls.Add(buttonHistory);
            panel1.Dock = DockStyle.Top;
            panel1.Location = new Point(0, 40);
            panel1.Margin = new Padding(0);
            panel1.Name = "panel1";
            panel1.Size = new Size(350, 40);
            panel1.TabIndex = 2;
            // 
            // menuButton
            // 
            menuButton.Dock = DockStyle.Left;
            menuButton.FlatAppearance.BorderSize = 0;
            menuButton.FlatAppearance.MouseOverBackColor = Color.Red;
            menuButton.FlatStyle = FlatStyle.Flat;
            menuButton.Font = new Font("Gadugi", 12F, FontStyle.Regular, GraphicsUnit.Point, 0);
            menuButton.ForeColor = Color.Transparent;
            menuButton.IconChar = FontAwesome.Sharp.IconChar.AlignJustify;
            menuButton.IconColor = Color.White;
            menuButton.IconFont = FontAwesome.Sharp.IconFont.Auto;
            menuButton.IconSize = 25;
            menuButton.Location = new Point(0, 0);
            menuButton.Margin = new Padding(0);
            menuButton.Name = "menuButton";
            menuButton.Size = new Size(50, 40);
            menuButton.TabIndex = 4;
            menuButton.UseVisualStyleBackColor = true;
            // 
            // buttonHistory
            // 
            buttonHistory.Dock = DockStyle.Right;
            buttonHistory.FlatAppearance.BorderSize = 0;
            buttonHistory.FlatAppearance.MouseOverBackColor = Color.Red;
            buttonHistory.FlatStyle = FlatStyle.Flat;
            buttonHistory.ForeColor = Color.Transparent;
            buttonHistory.IconChar = FontAwesome.Sharp.IconChar.ClockRotateLeft;
            buttonHistory.IconColor = Color.White;
            buttonHistory.IconFont = FontAwesome.Sharp.IconFont.Auto;
            buttonHistory.IconSize = 25;
            buttonHistory.Location = new Point(300, 0);
            buttonHistory.Margin = new Padding(0);
            buttonHistory.Name = "buttonHistory";
            buttonHistory.Size = new Size(50, 40);
            buttonHistory.TabIndex = 2;
            buttonHistory.UseVisualStyleBackColor = true;
            // 
            // textDisplay2
            // 
            textDisplay2.BackColor = Color.FromArgb(32, 32, 32);
            textDisplay2.BorderStyle = BorderStyle.None;
            textDisplay2.Dock = DockStyle.Top;
            textDisplay2.Font = new Font("Gadugi", 13.8F, FontStyle.Regular, GraphicsUnit.Point, 0);
            textDisplay2.ForeColor = Color.DarkGray;
            textDisplay2.Location = new Point(0, 80);
            textDisplay2.Margin = new Padding(0);
            textDisplay2.Multiline = true;
            textDisplay2.Name = "textDisplay2";
            textDisplay2.Size = new Size(350, 25);
            textDisplay2.TabIndex = 3;
            textDisplay2.Text = "0";
            textDisplay2.TextAlign = HorizontalAlignment.Right;
            // 
            // textDisplay1
            // 
            textDisplay1.BackColor = Color.FromArgb(32, 32, 32);
            textDisplay1.BorderStyle = BorderStyle.None;
            textDisplay1.Dock = DockStyle.Top;
            textDisplay1.Font = new Font("Gadugi", 30F, FontStyle.Bold);
            textDisplay1.ForeColor = Color.DarkGray;
            textDisplay1.Location = new Point(0, 105);
            textDisplay1.Margin = new Padding(0);
            textDisplay1.Multiline = true;
            textDisplay1.Name = "textDisplay1";
            textDisplay1.Size = new Size(350, 60);
            textDisplay1.TabIndex = 4;
            textDisplay1.Text = "0";
            textDisplay1.TextAlign = HorizontalAlignment.Right;
            // 
            // richTextBox1
            // 
            richTextBox1.BackColor = Color.FromArgb(32, 32, 32);
            richTextBox1.BorderStyle = BorderStyle.None;
            richTextBox1.ForeColor = Color.Silver;
            richTextBox1.Location = new Point(121, 12);
            richTextBox1.Name = "richTextBox1";
            richTextBox1.Size = new Size(169, 16);
            richTextBox1.TabIndex = 0;
            richTextBox1.Text = "";
            // 
            // CalculatorView
            // 
            AutoScaleMode = AutoScaleMode.None;
            BackColor = Color.FromArgb(32, 32, 32);
            ClientSize = new Size(350, 570);
            Controls.Add(textDisplay1);
            Controls.Add(textDisplay2);
            Controls.Add(panel1);
            Controls.Add(panelHistory);
            Controls.Add(panelTitle);
            Font = new Font("Gadugi", 12F, FontStyle.Regular, GraphicsUnit.Point, 0);
            ForeColor = Color.White;
            FormBorderStyle = FormBorderStyle.None;
            Name = "CalculatorView";
            StartPosition = FormStartPosition.CenterScreen;
            Text = "CalculatorView";
            panelTitle.ResumeLayout(false);
            panelHistory.ResumeLayout(false);
            panel1.ResumeLayout(false);
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Panel panelTitle;
        private Panel panelHistory;
        private Button button1;
        private FontAwesome.Sharp.IconButton buttonExit;
        private FontAwesome.Sharp.IconButton iconButton2;
        private FontAwesome.Sharp.IconButton iconButton1;
        private Panel panel1;
        private FontAwesome.Sharp.IconButton menuButton;
        private FontAwesome.Sharp.IconButton buttonHistory;
        private TextBox textDisplay2;
        private TextBox textDisplay1;
        private RichTextBox richTextBox1;
    }
}