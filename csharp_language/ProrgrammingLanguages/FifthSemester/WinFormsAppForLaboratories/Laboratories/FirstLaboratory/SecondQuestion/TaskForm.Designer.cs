namespace WinFormsAppForLaboratories.Laboratories.FirstLaboratory.SecondQuestion
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
            SwapToSecondForm = new Button();
            SuspendLayout();
            // 
            // SwapToSecondForm
            // 
            SwapToSecondForm.Location = new Point(289, 149);
            SwapToSecondForm.Name = "SwapToSecondForm";
            SwapToSecondForm.Size = new Size(239, 103);
            SwapToSecondForm.TabIndex = 0;
            SwapToSecondForm.Text = "Переключиться на другую форму";
            SwapToSecondForm.UseVisualStyleBackColor = true;
            SwapToSecondForm.Click += SwapToSecondForm_Click;
            // 
            // TaskForm
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(800, 450);
            Controls.Add(SwapToSecondForm);
            Name = "TaskForm";
            Text = "Ковалев Данил ВКБ22";
            ResumeLayout(false);
        }

        #endregion

        private Button SwapToSecondForm;
    }
}