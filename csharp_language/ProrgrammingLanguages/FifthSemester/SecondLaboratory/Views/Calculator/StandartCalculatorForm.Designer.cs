namespace SecondLaboratory.Views.Calculator
{
    partial class StandartCalculatorForm
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
            this.panel1 = new System.Windows.Forms.Panel();
            this.OperationHistoryLabel = new System.Windows.Forms.Label();
            this.panel2 = new System.Windows.Forms.Panel();
            this.OperationLabel = new System.Windows.Forms.Label();
            this.panel1.SuspendLayout();
            this.panel2.SuspendLayout();
            this.SuspendLayout();
            // 
            // panel1
            // 
            this.panel1.Controls.Add(this.OperationHistoryLabel);
            this.panel1.Dock = System.Windows.Forms.DockStyle.Top;
            this.panel1.Location = new System.Drawing.Point(0, 0);
            this.panel1.Name = "panel1";
            this.panel1.Size = new System.Drawing.Size(687, 36);
            this.panel1.TabIndex = 0;
            // 
            // OperationHistoryLabel
            // 
            this.OperationHistoryLabel.AutoSize = true;
            this.OperationHistoryLabel.Dock = System.Windows.Forms.DockStyle.Right;
            this.OperationHistoryLabel.ForeColor = System.Drawing.Color.DarkGray;
            this.OperationHistoryLabel.Location = new System.Drawing.Point(520, 0);
            this.OperationHistoryLabel.Name = "OperationHistoryLabel";
            this.OperationHistoryLabel.Size = new System.Drawing.Size(167, 20);
            this.OperationHistoryLabel.TabIndex = 0;
            this.OperationHistoryLabel.Text = "OperationHistoryLabel";
            this.OperationHistoryLabel.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // panel2
            // 
            this.panel2.Controls.Add(this.OperationLabel);
            this.panel2.Dock = System.Windows.Forms.DockStyle.Top;
            this.panel2.Location = new System.Drawing.Point(0, 36);
            this.panel2.Name = "panel2";
            this.panel2.Size = new System.Drawing.Size(687, 73);
            this.panel2.TabIndex = 0;
            // 
            // OperationLabel
            // 
            this.OperationLabel.AutoSize = true;
            this.OperationLabel.Dock = System.Windows.Forms.DockStyle.Right;
            this.OperationLabel.Font = new System.Drawing.Font("Microsoft Sans Serif", 24F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(204)));
            this.OperationLabel.ForeColor = System.Drawing.Color.White;
            this.OperationLabel.Location = new System.Drawing.Point(320, 0);
            this.OperationLabel.Name = "OperationLabel";
            this.OperationLabel.Size = new System.Drawing.Size(367, 55);
            this.OperationLabel.TabIndex = 0;
            this.OperationLabel.Text = "OperationLabel";
            this.OperationLabel.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // StandartCalculatorForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(9F, 20F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(20)))), ((int)(((byte)(20)))), ((int)(((byte)(20)))));
            this.ClientSize = new System.Drawing.Size(687, 871);
            this.Controls.Add(this.panel2);
            this.Controls.Add(this.panel1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.None;
            this.Name = "StandartCalculatorForm";
            this.Text = "StandartCalculatorForm";
            this.Load += new System.EventHandler(this.StandartCalculatorForm_Load);
            this.panel1.ResumeLayout(false);
            this.panel1.PerformLayout();
            this.panel2.ResumeLayout(false);
            this.panel2.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Panel panel1;
        private System.Windows.Forms.Label OperationHistoryLabel;
        private System.Windows.Forms.Panel panel2;
        private System.Windows.Forms.Label OperationLabel;
    }
}