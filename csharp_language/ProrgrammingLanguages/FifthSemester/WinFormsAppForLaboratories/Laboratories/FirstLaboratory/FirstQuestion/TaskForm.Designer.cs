namespace WinFormsAppForLaboratories.Laboratories.FirstLaboratory.FirstQuestion
{
    partial class TaskForm
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
            ExitButton = new Button();
            SuspendLayout();
            // 
            // ExitButton
            // 
            ExitButton.Location = new Point(312, 162);
            ExitButton.Name = "ExitButton";
            ExitButton.Size = new Size(198, 78);
            ExitButton.TabIndex = 0;
            ExitButton.Text = "Закрыть приложение";
            ExitButton.UseVisualStyleBackColor = true;
            ExitButton.Click += ExitButton_Click;
            // 
            // TaskForm
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(800, 450);
            Controls.Add(ExitButton);
            FormBorderStyle = FormBorderStyle.None;
            Name = "TaskForm";
            Text = "TaskForm";
            ResumeLayout(false);
        }

        #endregion

        private Button ExitButton;
    }
}