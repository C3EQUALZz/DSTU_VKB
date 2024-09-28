namespace ThirdLaboratory.forms
{
    partial class FormFirstQuestion
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(FormFirstQuestion));
            this.flowLayoutPanel1 = new System.Windows.Forms.FlowLayoutPanel();
            this.executeButton = new ReaLTaiizor.Controls.MaterialButton();
            this.clearButton = new ReaLTaiizor.Controls.MaterialButton();
            this.panel1 = new System.Windows.Forms.Panel();
            this.roundedPanel1 = new ThirdLaboratory.core.classes.RoundedPanel();
            this.label1 = new System.Windows.Forms.Label();
            this.panel2 = new System.Windows.Forms.Panel();
            this.tableLayoutPanel1 = new System.Windows.Forms.TableLayoutPanel();
            this.roundedPanel2 = new ThirdLaboratory.core.classes.RoundedPanel();
            this.label2 = new System.Windows.Forms.Label();
            this.tableLayoutPanel2 = new System.Windows.Forms.TableLayoutPanel();
            this.roundedPanel3 = new ThirdLaboratory.core.classes.RoundedPanel();
            this.resultLabel = new System.Windows.Forms.Label();
            this.roundedPanel4 = new ThirdLaboratory.core.classes.RoundedPanel();
            this.tableLayoutPanel3 = new System.Windows.Forms.TableLayoutPanel();
            this.lengthOfArrayInput = new ThirdLaboratory.core.classes.RJTextBox();
            this.startSliceOfArrayInput = new ThirdLaboratory.core.classes.RJTextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.label6 = new System.Windows.Forms.Label();
            this.endSliceOfArrayInput = new ThirdLaboratory.core.classes.RJTextBox();
            this.arrayOfRandomNumbersLabel = new System.Windows.Forms.Label();
            this.flowLayoutPanel1.SuspendLayout();
            this.panel1.SuspendLayout();
            this.roundedPanel1.SuspendLayout();
            this.panel2.SuspendLayout();
            this.tableLayoutPanel1.SuspendLayout();
            this.roundedPanel2.SuspendLayout();
            this.tableLayoutPanel2.SuspendLayout();
            this.roundedPanel3.SuspendLayout();
            this.roundedPanel4.SuspendLayout();
            this.tableLayoutPanel3.SuspendLayout();
            this.SuspendLayout();
            // 
            // flowLayoutPanel1
            // 
            this.flowLayoutPanel1.AutoSize = true;
            this.flowLayoutPanel1.Controls.Add(this.executeButton);
            this.flowLayoutPanel1.Controls.Add(this.clearButton);
            this.flowLayoutPanel1.Dock = System.Windows.Forms.DockStyle.Bottom;
            this.flowLayoutPanel1.FlowDirection = System.Windows.Forms.FlowDirection.RightToLeft;
            this.flowLayoutPanel1.Location = new System.Drawing.Point(0, 407);
            this.flowLayoutPanel1.Margin = new System.Windows.Forms.Padding(2);
            this.flowLayoutPanel1.Name = "flowLayoutPanel1";
            this.flowLayoutPanel1.Size = new System.Drawing.Size(532, 46);
            this.flowLayoutPanel1.TabIndex = 1;
            this.flowLayoutPanel1.WrapContents = false;
            // 
            // executeButton
            // 
            this.executeButton.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.executeButton.Density = ReaLTaiizor.Controls.MaterialButton.MaterialButtonDensity.Default;
            this.executeButton.Depth = 0;
            this.executeButton.HighEmphasis = true;
            this.executeButton.Icon = null;
            this.executeButton.IconType = ReaLTaiizor.Controls.MaterialButton.MaterialIconType.Rebase;
            this.executeButton.Location = new System.Drawing.Point(422, 5);
            this.executeButton.Margin = new System.Windows.Forms.Padding(3, 5, 3, 5);
            this.executeButton.MouseState = ReaLTaiizor.Helper.MaterialDrawHelper.MaterialMouseState.HOVER;
            this.executeButton.Name = "executeButton";
            this.executeButton.NoAccentTextColor = System.Drawing.Color.Empty;
            this.executeButton.Size = new System.Drawing.Size(107, 36);
            this.executeButton.TabIndex = 2;
            this.executeButton.Text = "Запустить";
            this.executeButton.Type = ReaLTaiizor.Controls.MaterialButton.MaterialButtonType.Contained;
            this.executeButton.UseAccentColor = false;
            this.executeButton.UseVisualStyleBackColor = true;
            this.executeButton.Click += new System.EventHandler(this.ExecuteButton_Click);
            // 
            // clearButton
            // 
            this.clearButton.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.clearButton.Density = ReaLTaiizor.Controls.MaterialButton.MaterialButtonDensity.Default;
            this.clearButton.Depth = 0;
            this.clearButton.HighEmphasis = true;
            this.clearButton.Icon = null;
            this.clearButton.IconType = ReaLTaiizor.Controls.MaterialButton.MaterialIconType.Rebase;
            this.clearButton.Location = new System.Drawing.Point(317, 5);
            this.clearButton.Margin = new System.Windows.Forms.Padding(3, 5, 3, 5);
            this.clearButton.MouseState = ReaLTaiizor.Helper.MaterialDrawHelper.MaterialMouseState.HOVER;
            this.clearButton.Name = "clearButton";
            this.clearButton.NoAccentTextColor = System.Drawing.Color.Empty;
            this.clearButton.Size = new System.Drawing.Size(99, 36);
            this.clearButton.TabIndex = 3;
            this.clearButton.Text = "Очистить";
            this.clearButton.Type = ReaLTaiizor.Controls.MaterialButton.MaterialButtonType.Contained;
            this.clearButton.UseAccentColor = false;
            this.clearButton.UseVisualStyleBackColor = true;
            this.clearButton.Click += new System.EventHandler(this.ClearButton_Click);
            // 
            // panel1
            // 
            this.panel1.Controls.Add(this.roundedPanel1);
            this.panel1.Dock = System.Windows.Forms.DockStyle.Top;
            this.panel1.Location = new System.Drawing.Point(0, 0);
            this.panel1.Margin = new System.Windows.Forms.Padding(0);
            this.panel1.Name = "panel1";
            this.panel1.Padding = new System.Windows.Forms.Padding(4, 4, 4, 0);
            this.panel1.Size = new System.Drawing.Size(532, 74);
            this.panel1.TabIndex = 2;
            // 
            // roundedPanel1
            // 
            this.roundedPanel1.Controls.Add(this.label1);
            this.roundedPanel1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.roundedPanel1.Location = new System.Drawing.Point(4, 4);
            this.roundedPanel1.Margin = new System.Windows.Forms.Padding(0);
            this.roundedPanel1.Name = "roundedPanel1";
            this.roundedPanel1.Size = new System.Drawing.Size(524, 70);
            this.roundedPanel1.TabIndex = 0;
            // 
            // label1
            // 
            this.label1.BackColor = System.Drawing.Color.Transparent;
            this.label1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.label1.Font = new System.Drawing.Font("MS Reference Sans Serif", 24F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.Location = new System.Drawing.Point(0, 0);
            this.label1.Margin = new System.Windows.Forms.Padding(8, 8, 8, 8);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(524, 70);
            this.label1.TabIndex = 0;
            this.label1.Text = "Вариант 1";
            this.label1.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // panel2
            // 
            this.panel2.Controls.Add(this.tableLayoutPanel1);
            this.panel2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.panel2.Location = new System.Drawing.Point(0, 74);
            this.panel2.Name = "panel2";
            this.panel2.Size = new System.Drawing.Size(532, 333);
            this.panel2.TabIndex = 3;
            // 
            // tableLayoutPanel1
            // 
            this.tableLayoutPanel1.ColumnCount = 1;
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33.24343F));
            this.tableLayoutPanel1.Controls.Add(this.roundedPanel2, 0, 0);
            this.tableLayoutPanel1.Controls.Add(this.tableLayoutPanel2, 0, 1);
            this.tableLayoutPanel1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel1.Location = new System.Drawing.Point(0, 0);
            this.tableLayoutPanel1.Name = "tableLayoutPanel1";
            this.tableLayoutPanel1.RowCount = 2;
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 86F));
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 16F));
            this.tableLayoutPanel1.Size = new System.Drawing.Size(532, 333);
            this.tableLayoutPanel1.TabIndex = 0;
            // 
            // roundedPanel2
            // 
            this.roundedPanel2.Controls.Add(this.label2);
            this.roundedPanel2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.roundedPanel2.Location = new System.Drawing.Point(3, 14);
            this.roundedPanel2.Margin = new System.Windows.Forms.Padding(3, 14, 3, 3);
            this.roundedPanel2.Name = "roundedPanel2";
            this.roundedPanel2.Size = new System.Drawing.Size(526, 69);
            this.roundedPanel2.TabIndex = 0;
            // 
            // label2
            // 
            this.label2.BackColor = System.Drawing.Color.Transparent;
            this.label2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.label2.Font = new System.Drawing.Font("Segoe UI", 7.8F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label2.Location = new System.Drawing.Point(0, 0);
            this.label2.Margin = new System.Windows.Forms.Padding(6, 0, 6, 0);
            this.label2.Name = "label2";
            this.label2.Padding = new System.Windows.Forms.Padding(16, 14, 16, 14);
            this.label2.Size = new System.Drawing.Size(526, 69);
            this.label2.TabIndex = 0;
            this.label2.Text = resources.GetString("label2.Text");
            // 
            // tableLayoutPanel2
            // 
            this.tableLayoutPanel2.ColumnCount = 1;
            this.tableLayoutPanel2.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.tableLayoutPanel2.Controls.Add(this.roundedPanel3, 0, 1);
            this.tableLayoutPanel2.Controls.Add(this.roundedPanel4, 0, 0);
            this.tableLayoutPanel2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel2.Location = new System.Drawing.Point(3, 89);
            this.tableLayoutPanel2.Name = "tableLayoutPanel2";
            this.tableLayoutPanel2.RowCount = 2;
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 62.5F));
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 37.5F));
            this.tableLayoutPanel2.Size = new System.Drawing.Size(526, 241);
            this.tableLayoutPanel2.TabIndex = 1;
            // 
            // roundedPanel3
            // 
            this.roundedPanel3.Controls.Add(this.resultLabel);
            this.roundedPanel3.Dock = System.Windows.Forms.DockStyle.Fill;
            this.roundedPanel3.Location = new System.Drawing.Point(3, 153);
            this.roundedPanel3.Name = "roundedPanel3";
            this.roundedPanel3.Size = new System.Drawing.Size(520, 85);
            this.roundedPanel3.TabIndex = 0;
            // 
            // resultLabel
            // 
            this.resultLabel.BackColor = System.Drawing.Color.Transparent;
            this.resultLabel.Dock = System.Windows.Forms.DockStyle.Fill;
            this.resultLabel.Font = new System.Drawing.Font("Segoe UI", 7.8F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.resultLabel.Location = new System.Drawing.Point(0, 0);
            this.resultLabel.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.resultLabel.Name = "resultLabel";
            this.resultLabel.Padding = new System.Windows.Forms.Padding(12, 12, 12, 12);
            this.resultLabel.Size = new System.Drawing.Size(520, 85);
            this.resultLabel.TabIndex = 0;
            this.resultLabel.Text = "Результат";
            // 
            // roundedPanel4
            // 
            this.roundedPanel4.Controls.Add(this.tableLayoutPanel3);
            this.roundedPanel4.Dock = System.Windows.Forms.DockStyle.Fill;
            this.roundedPanel4.Location = new System.Drawing.Point(3, 3);
            this.roundedPanel4.Name = "roundedPanel4";
            this.roundedPanel4.Size = new System.Drawing.Size(520, 144);
            this.roundedPanel4.TabIndex = 1;
            // 
            // tableLayoutPanel3
            // 
            this.tableLayoutPanel3.BackColor = System.Drawing.Color.Transparent;
            this.tableLayoutPanel3.ColumnCount = 2;
            this.tableLayoutPanel3.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanel3.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanel3.Controls.Add(this.lengthOfArrayInput, 1, 0);
            this.tableLayoutPanel3.Controls.Add(this.startSliceOfArrayInput, 1, 1);
            this.tableLayoutPanel3.Controls.Add(this.label3, 0, 0);
            this.tableLayoutPanel3.Controls.Add(this.label4, 0, 1);
            this.tableLayoutPanel3.Controls.Add(this.label5, 0, 2);
            this.tableLayoutPanel3.Controls.Add(this.label6, 0, 3);
            this.tableLayoutPanel3.Controls.Add(this.endSliceOfArrayInput, 1, 2);
            this.tableLayoutPanel3.Controls.Add(this.arrayOfRandomNumbersLabel, 1, 3);
            this.tableLayoutPanel3.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel3.Location = new System.Drawing.Point(0, 0);
            this.tableLayoutPanel3.Margin = new System.Windows.Forms.Padding(2);
            this.tableLayoutPanel3.Name = "tableLayoutPanel3";
            this.tableLayoutPanel3.RowCount = 4;
            this.tableLayoutPanel3.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 24.99553F));
            this.tableLayoutPanel3.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 24.99941F));
            this.tableLayoutPanel3.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 25.00192F));
            this.tableLayoutPanel3.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 25.00315F));
            this.tableLayoutPanel3.Size = new System.Drawing.Size(520, 144);
            this.tableLayoutPanel3.TabIndex = 2;
            // 
            // lengthOfArrayInput
            // 
            this.lengthOfArrayInput.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.lengthOfArrayInput.BackColor = System.Drawing.SystemColors.Window;
            this.lengthOfArrayInput.BorderColor = System.Drawing.Color.MediumSlateBlue;
            this.lengthOfArrayInput.BorderFocusColor = System.Drawing.Color.HotPink;
            this.lengthOfArrayInput.BorderRadius = 10;
            this.lengthOfArrayInput.BorderSize = 2;
            this.lengthOfArrayInput.Font = new System.Drawing.Font("Segoe UI", 10.2F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lengthOfArrayInput.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(64)))), ((int)(((byte)(64)))), ((int)(((byte)(64)))));
            this.lengthOfArrayInput.Location = new System.Drawing.Point(263, 3);
            this.lengthOfArrayInput.Multiline = false;
            this.lengthOfArrayInput.Name = "lengthOfArrayInput";
            this.lengthOfArrayInput.Padding = new System.Windows.Forms.Padding(8, 6, 8, 6);
            this.lengthOfArrayInput.PasswordChar = false;
            this.lengthOfArrayInput.PlaceholderColor = System.Drawing.Color.DarkGray;
            this.lengthOfArrayInput.PlaceholderText = "Введите такое N, что 1 < K <= L <= N";
            this.lengthOfArrayInput.Size = new System.Drawing.Size(254, 32);
            this.lengthOfArrayInput.TabIndex = 2;
            this.lengthOfArrayInput.Texts = "";
            this.lengthOfArrayInput.UnderlinedStyle = false;
            this.lengthOfArrayInput._TextChanged += new System.EventHandler(this.LengthOfArrayInput__TextChanged);
            // 
            // startSliceOfArrayInput
            // 
            this.startSliceOfArrayInput.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.startSliceOfArrayInput.BackColor = System.Drawing.SystemColors.Window;
            this.startSliceOfArrayInput.BorderColor = System.Drawing.Color.MediumSlateBlue;
            this.startSliceOfArrayInput.BorderFocusColor = System.Drawing.Color.HotPink;
            this.startSliceOfArrayInput.BorderRadius = 10;
            this.startSliceOfArrayInput.BorderSize = 2;
            this.startSliceOfArrayInput.Font = new System.Drawing.Font("Segoe UI", 10.2F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.startSliceOfArrayInput.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(64)))), ((int)(((byte)(64)))), ((int)(((byte)(64)))));
            this.startSliceOfArrayInput.Location = new System.Drawing.Point(263, 38);
            this.startSliceOfArrayInput.Multiline = false;
            this.startSliceOfArrayInput.Name = "startSliceOfArrayInput";
            this.startSliceOfArrayInput.Padding = new System.Windows.Forms.Padding(8, 6, 8, 6);
            this.startSliceOfArrayInput.PasswordChar = false;
            this.startSliceOfArrayInput.PlaceholderColor = System.Drawing.Color.DarkGray;
            this.startSliceOfArrayInput.PlaceholderText = "Введите такое K, что 1 < K <= L <= N ";
            this.startSliceOfArrayInput.Size = new System.Drawing.Size(254, 32);
            this.startSliceOfArrayInput.TabIndex = 0;
            this.startSliceOfArrayInput.Texts = "";
            this.startSliceOfArrayInput.UnderlinedStyle = false;
            this.startSliceOfArrayInput._TextChanged += new System.EventHandler(this.StartSliceOfArrayInput__TextChanged);
            // 
            // label3
            // 
            this.label3.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.label3.AutoSize = true;
            this.label3.Font = new System.Drawing.Font("Segoe UI", 7.8F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label3.Location = new System.Drawing.Point(53, 11);
            this.label3.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(154, 13);
            this.label3.TabIndex = 1;
            this.label3.Text = "Введите N (размер массива)";
            this.label3.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // label4
            // 
            this.label4.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.label4.AutoSize = true;
            this.label4.Font = new System.Drawing.Font("Segoe UI", 7.8F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label4.Location = new System.Drawing.Point(36, 46);
            this.label4.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(187, 13);
            this.label4.TabIndex = 3;
            this.label4.Text = "Введите K (начало среза включая)";
            // 
            // label5
            // 
            this.label5.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.label5.AutoSize = true;
            this.label5.Font = new System.Drawing.Font("Segoe UI", 7.8F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label5.Location = new System.Drawing.Point(40, 81);
            this.label5.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(180, 13);
            this.label5.TabIndex = 4;
            this.label5.Text = "Введите L (конец среза включая)";
            // 
            // label6
            // 
            this.label6.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.label6.AutoSize = true;
            this.label6.Font = new System.Drawing.Font("Segoe UI", 7.8F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label6.Location = new System.Drawing.Point(60, 118);
            this.label6.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(139, 13);
            this.label6.TabIndex = 5;
            this.label6.Text = "Массив случайных чисел";
            // 
            // endSliceOfArrayInput
            // 
            this.endSliceOfArrayInput.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.endSliceOfArrayInput.BackColor = System.Drawing.SystemColors.Window;
            this.endSliceOfArrayInput.BorderColor = System.Drawing.Color.MediumSlateBlue;
            this.endSliceOfArrayInput.BorderFocusColor = System.Drawing.Color.HotPink;
            this.endSliceOfArrayInput.BorderRadius = 10;
            this.endSliceOfArrayInput.BorderSize = 2;
            this.endSliceOfArrayInput.Font = new System.Drawing.Font("Segoe UI", 10.2F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.endSliceOfArrayInput.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(64)))), ((int)(((byte)(64)))), ((int)(((byte)(64)))));
            this.endSliceOfArrayInput.Location = new System.Drawing.Point(264, 73);
            this.endSliceOfArrayInput.Multiline = false;
            this.endSliceOfArrayInput.Name = "endSliceOfArrayInput";
            this.endSliceOfArrayInput.Padding = new System.Windows.Forms.Padding(8, 6, 8, 6);
            this.endSliceOfArrayInput.PasswordChar = false;
            this.endSliceOfArrayInput.PlaceholderColor = System.Drawing.Color.DarkGray;
            this.endSliceOfArrayInput.PlaceholderText = "Введите такое L, что 1 < K <= L <= N";
            this.endSliceOfArrayInput.Size = new System.Drawing.Size(252, 32);
            this.endSliceOfArrayInput.TabIndex = 6;
            this.endSliceOfArrayInput.Texts = "";
            this.endSliceOfArrayInput.UnderlinedStyle = false;
            this.endSliceOfArrayInput._TextChanged += new System.EventHandler(this.EndSliceOfArrayInput__TextChanged);
            // 
            // arrayOfRandomNumbersLabel
            // 
            this.arrayOfRandomNumbersLabel.BackColor = System.Drawing.Color.Transparent;
            this.arrayOfRandomNumbersLabel.Dock = System.Windows.Forms.DockStyle.Fill;
            this.arrayOfRandomNumbersLabel.Font = new System.Drawing.Font("Segoe UI", 7.8F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.arrayOfRandomNumbersLabel.Location = new System.Drawing.Point(268, 114);
            this.arrayOfRandomNumbersLabel.Margin = new System.Windows.Forms.Padding(8, 8, 8, 8);
            this.arrayOfRandomNumbersLabel.Name = "arrayOfRandomNumbersLabel";
            this.arrayOfRandomNumbersLabel.Size = new System.Drawing.Size(244, 22);
            this.arrayOfRandomNumbersLabel.TabIndex = 7;
            this.arrayOfRandomNumbersLabel.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // FormFirstQuestion
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(96F, 96F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Dpi;
            this.ClientSize = new System.Drawing.Size(532, 453);
            this.Controls.Add(this.panel2);
            this.Controls.Add(this.panel1);
            this.Controls.Add(this.flowLayoutPanel1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.None;
            this.Margin = new System.Windows.Forms.Padding(2);
            this.Name = "FormFirstQuestion";
            this.Text = "FormFirstQuestioncs";
            this.flowLayoutPanel1.ResumeLayout(false);
            this.flowLayoutPanel1.PerformLayout();
            this.panel1.ResumeLayout(false);
            this.roundedPanel1.ResumeLayout(false);
            this.panel2.ResumeLayout(false);
            this.tableLayoutPanel1.ResumeLayout(false);
            this.roundedPanel2.ResumeLayout(false);
            this.tableLayoutPanel2.ResumeLayout(false);
            this.roundedPanel3.ResumeLayout(false);
            this.roundedPanel4.ResumeLayout(false);
            this.tableLayoutPanel3.ResumeLayout(false);
            this.tableLayoutPanel3.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion
        private System.Windows.Forms.FlowLayoutPanel flowLayoutPanel1;
        private ReaLTaiizor.Controls.MaterialButton executeButton;
        private ReaLTaiizor.Controls.MaterialButton clearButton;
        private System.Windows.Forms.Panel panel1;
        private core.classes.RoundedPanel roundedPanel1;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Panel panel2;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel1;
        private core.classes.RoundedPanel roundedPanel2;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel2;
        private core.classes.RoundedPanel roundedPanel3;
        private System.Windows.Forms.Label resultLabel;
        private core.classes.RoundedPanel roundedPanel4;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel3;
        private core.classes.RJTextBox lengthOfArrayInput;
        private core.classes.RJTextBox startSliceOfArrayInput;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Label label6;
        private core.classes.RJTextBox endSliceOfArrayInput;
        private System.Windows.Forms.Label arrayOfRandomNumbersLabel;
    }
}