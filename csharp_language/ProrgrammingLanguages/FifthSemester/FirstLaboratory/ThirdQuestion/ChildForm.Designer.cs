namespace FirstLaboratory.ThirdQuestion
{
    partial class ChildForm
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
            ChildTextBox = new RichTextBox();
            MenuStrip = new MenuStrip();
            FormatMenuItem = new ToolStripMenuItem();
            ToggleMenuItem = new ToolStripMenuItem();
            MenuStrip.SuspendLayout();
            SuspendLayout();
            // 
            // ChildTextBox
            // 
            ChildTextBox.Dock = DockStyle.Fill;
            ChildTextBox.Location = new Point(0, 28);
            ChildTextBox.Name = "ChildTextBox";
            ChildTextBox.Size = new Size(800, 422);
            ChildTextBox.TabIndex = 0;
            ChildTextBox.Text = "";
            // 
            // MenuStrip
            // 
            MenuStrip.ImageScalingSize = new Size(20, 20);
            MenuStrip.Items.AddRange(new ToolStripItem[] { FormatMenuItem });
            MenuStrip.Location = new Point(0, 0);
            MenuStrip.Name = "MenuStrip";
            MenuStrip.Size = new Size(800, 28);
            MenuStrip.TabIndex = 1;
            // 
            // FormatMenuItem
            // 
            FormatMenuItem.DropDownItems.AddRange(new ToolStripItem[] { ToggleMenuItem });
            FormatMenuItem.MergeAction = MergeAction.Insert;
            FormatMenuItem.Name = "FormatMenuItem";
            FormatMenuItem.Size = new Size(70, 24);
            FormatMenuItem.Text = "F&ormat";
            // 
            // ToggleMenuItem
            // 
            ToggleMenuItem.Name = "ToggleMenuItem";
            ToggleMenuItem.Size = new Size(224, 26);
            ToggleMenuItem.Text = "&Toggle Foreground";
            ToggleMenuItem.Click += ToggleMenuItem_Click;
            // 
            // ChildForm
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(800, 450);
            Controls.Add(ChildTextBox);
            Controls.Add(MenuStrip);
            MainMenuStrip = MenuStrip;
            Name = "ChildForm";
            Text = "Child Form";
            MenuStrip.ResumeLayout(false);
            MenuStrip.PerformLayout();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private RichTextBox ChildTextBox;
        private MenuStrip MenuStrip;
        private ToolStripMenuItem FormatMenuItem;
        private ToolStripMenuItem ToggleMenuItem;
    }
}