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
            this.panel3 = new System.Windows.Forms.Panel();
            this.panel4 = new System.Windows.Forms.Panel();
            this.tableLayoutPanel1 = new System.Windows.Forms.TableLayoutPanel();
            this.MCButton = new System.Windows.Forms.Button();
            this.MRButton = new System.Windows.Forms.Button();
            this.MSButton = new System.Windows.Forms.Button();
            this.MPButton = new System.Windows.Forms.Button();
            this.MMButton = new System.Windows.Forms.Button();
            this.panel1.SuspendLayout();
            this.panel2.SuspendLayout();
            this.panel3.SuspendLayout();
            this.tableLayoutPanel1.SuspendLayout();
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
            // panel3
            // 
            this.panel3.Controls.Add(this.tableLayoutPanel1);
            this.panel3.Dock = System.Windows.Forms.DockStyle.Top;
            this.panel3.Location = new System.Drawing.Point(0, 109);
            this.panel3.Name = "panel3";
            this.panel3.Size = new System.Drawing.Size(687, 46);
            this.panel3.TabIndex = 1;
            // 
            // panel4
            // 
            this.panel4.Dock = System.Windows.Forms.DockStyle.Fill;
            this.panel4.Location = new System.Drawing.Point(0, 155);
            this.panel4.Name = "panel4";
            this.panel4.Size = new System.Drawing.Size(687, 716);
            this.panel4.TabIndex = 2;
            // 
            // tableLayoutPanel1
            // 
            this.tableLayoutPanel1.ColumnCount = 5;
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 20F));
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 20F));
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 20F));
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 20F));
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 20F));
            this.tableLayoutPanel1.Controls.Add(this.MMButton, 4, 0);
            this.tableLayoutPanel1.Controls.Add(this.MPButton, 3, 0);
            this.tableLayoutPanel1.Controls.Add(this.MSButton, 2, 0);
            this.tableLayoutPanel1.Controls.Add(this.MRButton, 1, 0);
            this.tableLayoutPanel1.Controls.Add(this.MCButton, 0, 0);
            this.tableLayoutPanel1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel1.Location = new System.Drawing.Point(0, 0);
            this.tableLayoutPanel1.Name = "tableLayoutPanel1";
            this.tableLayoutPanel1.RowCount = 1;
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.tableLayoutPanel1.Size = new System.Drawing.Size(687, 46);
            this.tableLayoutPanel1.TabIndex = 0;
            // 
            // MCButton
            // 
            this.MCButton.Dock = System.Windows.Forms.DockStyle.Fill;
            this.MCButton.FlatAppearance.BorderSize = 0;
            this.MCButton.FlatAppearance.MouseDownBackColor = System.Drawing.Color.FromArgb(((int)(((byte)(50)))), ((int)(((byte)(50)))), ((int)(((byte)(50)))));
            this.MCButton.FlatAppearance.MouseOverBackColor = System.Drawing.Color.FromArgb(((int)(((byte)(30)))), ((int)(((byte)(30)))), ((int)(((byte)(30)))));
            this.MCButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.MCButton.ForeColor = System.Drawing.Color.White;
            this.MCButton.Location = new System.Drawing.Point(10, 10);
            this.MCButton.Margin = new System.Windows.Forms.Padding(10);
            this.MCButton.Name = "MCButton";
            this.MCButton.Size = new System.Drawing.Size(117, 26);
            this.MCButton.TabIndex = 0;
            this.MCButton.Text = "MC";
            this.MCButton.UseVisualStyleBackColor = true;
            // 
            // MRButton
            // 
            this.MRButton.Dock = System.Windows.Forms.DockStyle.Fill;
            this.MRButton.FlatAppearance.BorderSize = 0;
            this.MRButton.FlatAppearance.MouseDownBackColor = System.Drawing.Color.FromArgb(((int)(((byte)(50)))), ((int)(((byte)(50)))), ((int)(((byte)(50)))));
            this.MRButton.FlatAppearance.MouseOverBackColor = System.Drawing.Color.FromArgb(((int)(((byte)(30)))), ((int)(((byte)(30)))), ((int)(((byte)(30)))));
            this.MRButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.MRButton.ForeColor = System.Drawing.Color.White;
            this.MRButton.Location = new System.Drawing.Point(147, 10);
            this.MRButton.Margin = new System.Windows.Forms.Padding(10);
            this.MRButton.Name = "MRButton";
            this.MRButton.Size = new System.Drawing.Size(117, 26);
            this.MRButton.TabIndex = 1;
            this.MRButton.Text = "MR";
            this.MRButton.UseVisualStyleBackColor = true;
            // 
            // MSButton
            // 
            this.MSButton.Dock = System.Windows.Forms.DockStyle.Fill;
            this.MSButton.FlatAppearance.BorderSize = 0;
            this.MSButton.FlatAppearance.MouseDownBackColor = System.Drawing.Color.FromArgb(((int)(((byte)(50)))), ((int)(((byte)(50)))), ((int)(((byte)(50)))));
            this.MSButton.FlatAppearance.MouseOverBackColor = System.Drawing.Color.FromArgb(((int)(((byte)(30)))), ((int)(((byte)(30)))), ((int)(((byte)(30)))));
            this.MSButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.MSButton.ForeColor = System.Drawing.Color.White;
            this.MSButton.Location = new System.Drawing.Point(284, 10);
            this.MSButton.Margin = new System.Windows.Forms.Padding(10);
            this.MSButton.Name = "MSButton";
            this.MSButton.Size = new System.Drawing.Size(117, 26);
            this.MSButton.TabIndex = 2;
            this.MSButton.Text = "MS";
            this.MSButton.UseVisualStyleBackColor = true;
            // 
            // MPButton
            // 
            this.MPButton.Dock = System.Windows.Forms.DockStyle.Fill;
            this.MPButton.FlatAppearance.BorderSize = 0;
            this.MPButton.FlatAppearance.MouseDownBackColor = System.Drawing.Color.FromArgb(((int)(((byte)(50)))), ((int)(((byte)(50)))), ((int)(((byte)(50)))));
            this.MPButton.FlatAppearance.MouseOverBackColor = System.Drawing.Color.FromArgb(((int)(((byte)(30)))), ((int)(((byte)(30)))), ((int)(((byte)(30)))));
            this.MPButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.MPButton.ForeColor = System.Drawing.Color.White;
            this.MPButton.Location = new System.Drawing.Point(421, 10);
            this.MPButton.Margin = new System.Windows.Forms.Padding(10);
            this.MPButton.Name = "MPButton";
            this.MPButton.Size = new System.Drawing.Size(117, 26);
            this.MPButton.TabIndex = 3;
            this.MPButton.Text = "M+";
            this.MPButton.UseVisualStyleBackColor = true;
            // 
            // MMButton
            // 
            this.MMButton.Dock = System.Windows.Forms.DockStyle.Fill;
            this.MMButton.FlatAppearance.BorderSize = 0;
            this.MMButton.FlatAppearance.MouseDownBackColor = System.Drawing.Color.FromArgb(((int)(((byte)(50)))), ((int)(((byte)(50)))), ((int)(((byte)(50)))));
            this.MMButton.FlatAppearance.MouseOverBackColor = System.Drawing.Color.FromArgb(((int)(((byte)(30)))), ((int)(((byte)(30)))), ((int)(((byte)(30)))));
            this.MMButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.MMButton.ForeColor = System.Drawing.Color.White;
            this.MMButton.Location = new System.Drawing.Point(558, 10);
            this.MMButton.Margin = new System.Windows.Forms.Padding(10);
            this.MMButton.Name = "MMButton";
            this.MMButton.Size = new System.Drawing.Size(119, 26);
            this.MMButton.TabIndex = 4;
            this.MMButton.Text = "M-";
            this.MMButton.UseVisualStyleBackColor = true;
            // 
            // StandartCalculatorForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(9F, 20F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(20)))), ((int)(((byte)(20)))), ((int)(((byte)(20)))));
            this.ClientSize = new System.Drawing.Size(687, 871);
            this.Controls.Add(this.panel4);
            this.Controls.Add(this.panel3);
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
            this.panel3.ResumeLayout(false);
            this.tableLayoutPanel1.ResumeLayout(false);
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Panel panel1;
        private System.Windows.Forms.Label OperationHistoryLabel;
        private System.Windows.Forms.Panel panel2;
        private System.Windows.Forms.Label OperationLabel;
        private System.Windows.Forms.Panel panel3;
        private System.Windows.Forms.Panel panel4;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel1;
        private System.Windows.Forms.Button MCButton;
        private System.Windows.Forms.Button MMButton;
        private System.Windows.Forms.Button MPButton;
        private System.Windows.Forms.Button MSButton;
        private System.Windows.Forms.Button MRButton;
    }
}