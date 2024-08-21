namespace ThirdLaboratory.forms
{
    partial class FormNineteenthQuestion
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
            this.executeButton = new ReaLTaiizor.Controls.MaterialButton();
            this.clearButton = new ReaLTaiizor.Controls.MaterialButton();
            this.flowLayoutPanel1 = new System.Windows.Forms.FlowLayoutPanel();
            this.panel1 = new System.Windows.Forms.Panel();
            this.roundedPanel1 = new ThirdLaboratory.core.classes.RoundedPanel();
            this.label1 = new System.Windows.Forms.Label();
            this.tableLayoutPanel1 = new System.Windows.Forms.TableLayoutPanel();
            this.roundedPanel2 = new ThirdLaboratory.core.classes.RoundedPanel();
            this.label2 = new System.Windows.Forms.Label();
            this.tableLayoutPanel2 = new System.Windows.Forms.TableLayoutPanel();
            this.tableLayoutPanel3 = new System.Windows.Forms.TableLayoutPanel();
            this.tableLayoutPanel5 = new System.Windows.Forms.TableLayoutPanel();
            this.tableLayoutPanel6 = new System.Windows.Forms.TableLayoutPanel();
            this.countOfColumnsInput = new ThirdLaboratory.core.classes.RJTextBox();
            this.numberOfDeletingColumn = new ThirdLaboratory.core.classes.RJTextBox();
            this.countOfRowsInput = new ThirdLaboratory.core.classes.RJTextBox();
            this.createMatrixButton = new ReaLTaiizor.Controls.MaterialButton();
            this.dataGridView = new System.Windows.Forms.DataGridView();
            this.flowLayoutPanel1.SuspendLayout();
            this.panel1.SuspendLayout();
            this.roundedPanel1.SuspendLayout();
            this.tableLayoutPanel1.SuspendLayout();
            this.roundedPanel2.SuspendLayout();
            this.tableLayoutPanel2.SuspendLayout();
            this.tableLayoutPanel3.SuspendLayout();
            this.tableLayoutPanel5.SuspendLayout();
            this.tableLayoutPanel6.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView)).BeginInit();
            this.SuspendLayout();
            // 
            // executeButton
            // 
            this.executeButton.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.executeButton.Density = ReaLTaiizor.Controls.MaterialButton.MaterialButtonDensity.Default;
            this.executeButton.Depth = 0;
            this.executeButton.HighEmphasis = true;
            this.executeButton.Icon = null;
            this.executeButton.IconType = ReaLTaiizor.Controls.MaterialButton.MaterialIconType.Rebase;
            this.executeButton.Location = new System.Drawing.Point(598, 6);
            this.executeButton.Margin = new System.Windows.Forms.Padding(4, 6, 4, 6);
            this.executeButton.MouseState = ReaLTaiizor.Helper.MaterialDrawHelper.MaterialMouseState.HOVER;
            this.executeButton.Name = "executeButton";
            this.executeButton.NoAccentTextColor = System.Drawing.Color.Empty;
            this.executeButton.Size = new System.Drawing.Size(107, 36);
            this.executeButton.TabIndex = 0;
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
            this.clearButton.Location = new System.Drawing.Point(491, 6);
            this.clearButton.Margin = new System.Windows.Forms.Padding(4, 6, 4, 6);
            this.clearButton.MouseState = ReaLTaiizor.Helper.MaterialDrawHelper.MaterialMouseState.HOVER;
            this.clearButton.Name = "clearButton";
            this.clearButton.NoAccentTextColor = System.Drawing.Color.Empty;
            this.clearButton.Size = new System.Drawing.Size(99, 36);
            this.clearButton.TabIndex = 1;
            this.clearButton.Text = "Очистить";
            this.clearButton.Type = ReaLTaiizor.Controls.MaterialButton.MaterialButtonType.Contained;
            this.clearButton.UseAccentColor = false;
            this.clearButton.UseVisualStyleBackColor = true;
            this.clearButton.Click += new System.EventHandler(this.ClearButton_Click);
            // 
            // flowLayoutPanel1
            // 
            this.flowLayoutPanel1.AutoSize = true;
            this.flowLayoutPanel1.Controls.Add(this.executeButton);
            this.flowLayoutPanel1.Controls.Add(this.clearButton);
            this.flowLayoutPanel1.Dock = System.Windows.Forms.DockStyle.Bottom;
            this.flowLayoutPanel1.FlowDirection = System.Windows.Forms.FlowDirection.RightToLeft;
            this.flowLayoutPanel1.Location = new System.Drawing.Point(0, 510);
            this.flowLayoutPanel1.Name = "flowLayoutPanel1";
            this.flowLayoutPanel1.Size = new System.Drawing.Size(709, 48);
            this.flowLayoutPanel1.TabIndex = 2;
            // 
            // panel1
            // 
            this.panel1.Controls.Add(this.roundedPanel1);
            this.panel1.Dock = System.Windows.Forms.DockStyle.Top;
            this.panel1.Location = new System.Drawing.Point(0, 0);
            this.panel1.Name = "panel1";
            this.panel1.Padding = new System.Windows.Forms.Padding(5, 5, 5, 0);
            this.panel1.Size = new System.Drawing.Size(709, 91);
            this.panel1.TabIndex = 3;
            // 
            // roundedPanel1
            // 
            this.roundedPanel1.Controls.Add(this.label1);
            this.roundedPanel1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.roundedPanel1.Location = new System.Drawing.Point(5, 5);
            this.roundedPanel1.Name = "roundedPanel1";
            this.roundedPanel1.Size = new System.Drawing.Size(699, 86);
            this.roundedPanel1.TabIndex = 0;
            // 
            // label1
            // 
            this.label1.BackColor = System.Drawing.Color.Transparent;
            this.label1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.label1.Font = new System.Drawing.Font("MS Reference Sans Serif", 24F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.Location = new System.Drawing.Point(0, 0);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(699, 86);
            this.label1.TabIndex = 0;
            this.label1.Text = "Вариант 19";
            this.label1.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // tableLayoutPanel1
            // 
            this.tableLayoutPanel1.ColumnCount = 1;
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.tableLayoutPanel1.Controls.Add(this.roundedPanel2, 0, 0);
            this.tableLayoutPanel1.Controls.Add(this.tableLayoutPanel2, 0, 1);
            this.tableLayoutPanel1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel1.Font = new System.Drawing.Font("Segoe UI", 7.8F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.tableLayoutPanel1.Location = new System.Drawing.Point(0, 91);
            this.tableLayoutPanel1.Name = "tableLayoutPanel1";
            this.tableLayoutPanel1.RowCount = 2;
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 20.59426F));
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 79.40574F));
            this.tableLayoutPanel1.Size = new System.Drawing.Size(709, 419);
            this.tableLayoutPanel1.TabIndex = 4;
            // 
            // roundedPanel2
            // 
            this.roundedPanel2.Controls.Add(this.label2);
            this.roundedPanel2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.roundedPanel2.Location = new System.Drawing.Point(3, 14);
            this.roundedPanel2.Margin = new System.Windows.Forms.Padding(3, 14, 3, 3);
            this.roundedPanel2.Name = "roundedPanel2";
            this.roundedPanel2.Size = new System.Drawing.Size(703, 69);
            this.roundedPanel2.TabIndex = 0;
            // 
            // label2
            // 
            this.label2.BackColor = System.Drawing.Color.Transparent;
            this.label2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.label2.Location = new System.Drawing.Point(0, 0);
            this.label2.Name = "label2";
            this.label2.Padding = new System.Windows.Forms.Padding(18, 20, 18, 20);
            this.label2.Size = new System.Drawing.Size(703, 69);
            this.label2.TabIndex = 0;
            this.label2.Text = "Дана матрица размера M × N и целое число K(1 ≤ K ≤ N). Удалить столбец матрицы с " +
    "номером K.";
            // 
            // tableLayoutPanel2
            // 
            this.tableLayoutPanel2.ColumnCount = 1;
            this.tableLayoutPanel2.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.tableLayoutPanel2.Controls.Add(this.tableLayoutPanel3, 0, 0);
            this.tableLayoutPanel2.Controls.Add(this.dataGridView, 0, 1);
            this.tableLayoutPanel2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel2.Location = new System.Drawing.Point(3, 89);
            this.tableLayoutPanel2.Name = "tableLayoutPanel2";
            this.tableLayoutPanel2.RowCount = 2;
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 36.22449F));
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 63.77551F));
            this.tableLayoutPanel2.Size = new System.Drawing.Size(703, 327);
            this.tableLayoutPanel2.TabIndex = 1;
            // 
            // tableLayoutPanel3
            // 
            this.tableLayoutPanel3.ColumnCount = 1;
            this.tableLayoutPanel3.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.tableLayoutPanel3.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 20F));
            this.tableLayoutPanel3.Controls.Add(this.tableLayoutPanel5, 0, 0);
            this.tableLayoutPanel3.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel3.Location = new System.Drawing.Point(3, 3);
            this.tableLayoutPanel3.Name = "tableLayoutPanel3";
            this.tableLayoutPanel3.RowCount = 1;
            this.tableLayoutPanel3.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.tableLayoutPanel3.Size = new System.Drawing.Size(697, 112);
            this.tableLayoutPanel3.TabIndex = 0;
            // 
            // tableLayoutPanel5
            // 
            this.tableLayoutPanel5.ColumnCount = 1;
            this.tableLayoutPanel5.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.tableLayoutPanel5.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 20F));
            this.tableLayoutPanel5.Controls.Add(this.tableLayoutPanel6, 0, 0);
            this.tableLayoutPanel5.Controls.Add(this.createMatrixButton, 0, 1);
            this.tableLayoutPanel5.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel5.Location = new System.Drawing.Point(3, 3);
            this.tableLayoutPanel5.Name = "tableLayoutPanel5";
            this.tableLayoutPanel5.RowCount = 2;
            this.tableLayoutPanel5.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanel5.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanel5.Size = new System.Drawing.Size(691, 106);
            this.tableLayoutPanel5.TabIndex = 1;
            // 
            // tableLayoutPanel6
            // 
            this.tableLayoutPanel6.ColumnCount = 3;
            this.tableLayoutPanel6.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33.33333F));
            this.tableLayoutPanel6.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33.33333F));
            this.tableLayoutPanel6.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33.33333F));
            this.tableLayoutPanel6.Controls.Add(this.countOfColumnsInput, 0, 0);
            this.tableLayoutPanel6.Controls.Add(this.numberOfDeletingColumn, 1, 0);
            this.tableLayoutPanel6.Controls.Add(this.countOfRowsInput, 0, 0);
            this.tableLayoutPanel6.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel6.Location = new System.Drawing.Point(3, 3);
            this.tableLayoutPanel6.Name = "tableLayoutPanel6";
            this.tableLayoutPanel6.RowCount = 1;
            this.tableLayoutPanel6.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.tableLayoutPanel6.Size = new System.Drawing.Size(685, 47);
            this.tableLayoutPanel6.TabIndex = 0;
            // 
            // countOfColumnsInput
            // 
            this.countOfColumnsInput.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.countOfColumnsInput.BackColor = System.Drawing.SystemColors.Window;
            this.countOfColumnsInput.BorderColor = System.Drawing.Color.MediumSlateBlue;
            this.countOfColumnsInput.BorderFocusColor = System.Drawing.Color.HotPink;
            this.countOfColumnsInput.BorderRadius = 10;
            this.countOfColumnsInput.BorderSize = 2;
            this.countOfColumnsInput.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.countOfColumnsInput.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(64)))), ((int)(((byte)(64)))), ((int)(((byte)(64)))));
            this.countOfColumnsInput.Location = new System.Drawing.Point(232, 6);
            this.countOfColumnsInput.Margin = new System.Windows.Forms.Padding(4);
            this.countOfColumnsInput.Multiline = false;
            this.countOfColumnsInput.Name = "countOfColumnsInput";
            this.countOfColumnsInput.Padding = new System.Windows.Forms.Padding(10, 7, 10, 7);
            this.countOfColumnsInput.PasswordChar = false;
            this.countOfColumnsInput.PlaceholderColor = System.Drawing.Color.DarkGray;
            this.countOfColumnsInput.PlaceholderText = "Введите N (кол-во столбцов)";
            this.countOfColumnsInput.Size = new System.Drawing.Size(220, 35);
            this.countOfColumnsInput.TabIndex = 2;
            this.countOfColumnsInput.Texts = "";
            this.countOfColumnsInput.UnderlinedStyle = false;
            this.countOfColumnsInput._TextChanged += new System.EventHandler(this.CountOfColumnsInput__TextChanged);
            // 
            // numberOfDeletingColumn
            // 
            this.numberOfDeletingColumn.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.numberOfDeletingColumn.BackColor = System.Drawing.SystemColors.Window;
            this.numberOfDeletingColumn.BorderColor = System.Drawing.Color.MediumSlateBlue;
            this.numberOfDeletingColumn.BorderFocusColor = System.Drawing.Color.HotPink;
            this.numberOfDeletingColumn.BorderRadius = 10;
            this.numberOfDeletingColumn.BorderSize = 2;
            this.numberOfDeletingColumn.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.numberOfDeletingColumn.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(64)))), ((int)(((byte)(64)))), ((int)(((byte)(64)))));
            this.numberOfDeletingColumn.Location = new System.Drawing.Point(460, 6);
            this.numberOfDeletingColumn.Margin = new System.Windows.Forms.Padding(4);
            this.numberOfDeletingColumn.Multiline = false;
            this.numberOfDeletingColumn.Name = "numberOfDeletingColumn";
            this.numberOfDeletingColumn.Padding = new System.Windows.Forms.Padding(10, 7, 10, 7);
            this.numberOfDeletingColumn.PasswordChar = false;
            this.numberOfDeletingColumn.PlaceholderColor = System.Drawing.Color.DarkGray;
            this.numberOfDeletingColumn.PlaceholderText = "Введите K (1 <= K <= N)";
            this.numberOfDeletingColumn.Size = new System.Drawing.Size(220, 35);
            this.numberOfDeletingColumn.TabIndex = 0;
            this.numberOfDeletingColumn.Texts = "";
            this.numberOfDeletingColumn.UnderlinedStyle = false;
            this.numberOfDeletingColumn._TextChanged += new System.EventHandler(this.NumberOfDeletingColumn__TextChanged);
            // 
            // countOfRowsInput
            // 
            this.countOfRowsInput.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.countOfRowsInput.BackColor = System.Drawing.SystemColors.Window;
            this.countOfRowsInput.BorderColor = System.Drawing.Color.MediumSlateBlue;
            this.countOfRowsInput.BorderFocusColor = System.Drawing.Color.HotPink;
            this.countOfRowsInput.BorderRadius = 10;
            this.countOfRowsInput.BorderSize = 2;
            this.countOfRowsInput.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.countOfRowsInput.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(64)))), ((int)(((byte)(64)))), ((int)(((byte)(64)))));
            this.countOfRowsInput.Location = new System.Drawing.Point(4, 6);
            this.countOfRowsInput.Margin = new System.Windows.Forms.Padding(4);
            this.countOfRowsInput.Multiline = false;
            this.countOfRowsInput.Name = "countOfRowsInput";
            this.countOfRowsInput.Padding = new System.Windows.Forms.Padding(10, 7, 10, 7);
            this.countOfRowsInput.PasswordChar = false;
            this.countOfRowsInput.PlaceholderColor = System.Drawing.Color.DarkGray;
            this.countOfRowsInput.PlaceholderText = "Введите M (кол-во строк)";
            this.countOfRowsInput.Size = new System.Drawing.Size(220, 35);
            this.countOfRowsInput.TabIndex = 1;
            this.countOfRowsInput.Texts = "";
            this.countOfRowsInput.UnderlinedStyle = false;
            this.countOfRowsInput._TextChanged += new System.EventHandler(this.CountOfRowsInput__TextChanged);
            // 
            // createMatrixButton
            // 
            this.createMatrixButton.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.createMatrixButton.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.createMatrixButton.Density = ReaLTaiizor.Controls.MaterialButton.MaterialButtonDensity.Default;
            this.createMatrixButton.Depth = 0;
            this.createMatrixButton.HighEmphasis = true;
            this.createMatrixButton.Icon = null;
            this.createMatrixButton.IconType = ReaLTaiizor.Controls.MaterialButton.MaterialIconType.Rebase;
            this.createMatrixButton.Location = new System.Drawing.Point(263, 61);
            this.createMatrixButton.Margin = new System.Windows.Forms.Padding(4, 6, 4, 6);
            this.createMatrixButton.MouseState = ReaLTaiizor.Helper.MaterialDrawHelper.MaterialMouseState.HOVER;
            this.createMatrixButton.Name = "createMatrixButton";
            this.createMatrixButton.NoAccentTextColor = System.Drawing.Color.Empty;
            this.createMatrixButton.Size = new System.Drawing.Size(164, 36);
            this.createMatrixButton.TabIndex = 1;
            this.createMatrixButton.Text = "Создать матрицу";
            this.createMatrixButton.Type = ReaLTaiizor.Controls.MaterialButton.MaterialButtonType.Contained;
            this.createMatrixButton.UseAccentColor = false;
            this.createMatrixButton.UseVisualStyleBackColor = true;
            this.createMatrixButton.Click += new System.EventHandler(this.CreateMatrixButton_Click);
            // 
            // dataGridView
            // 
            this.dataGridView.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridView.Dock = System.Windows.Forms.DockStyle.Fill;
            this.dataGridView.Location = new System.Drawing.Point(3, 121);
            this.dataGridView.Name = "dataGridView";
            this.dataGridView.RowHeadersWidth = 51;
            this.dataGridView.RowTemplate.Height = 24;
            this.dataGridView.Size = new System.Drawing.Size(697, 203);
            this.dataGridView.TabIndex = 1;
            // 
            // FormNineteenthQuestion
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(709, 558);
            this.Controls.Add(this.tableLayoutPanel1);
            this.Controls.Add(this.panel1);
            this.Controls.Add(this.flowLayoutPanel1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.None;
            this.Name = "FormNineteenthQuestion";
            this.Text = "FormNineteenthQuestion";
            this.flowLayoutPanel1.ResumeLayout(false);
            this.flowLayoutPanel1.PerformLayout();
            this.panel1.ResumeLayout(false);
            this.roundedPanel1.ResumeLayout(false);
            this.tableLayoutPanel1.ResumeLayout(false);
            this.roundedPanel2.ResumeLayout(false);
            this.tableLayoutPanel2.ResumeLayout(false);
            this.tableLayoutPanel3.ResumeLayout(false);
            this.tableLayoutPanel5.ResumeLayout(false);
            this.tableLayoutPanel5.PerformLayout();
            this.tableLayoutPanel6.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private ReaLTaiizor.Controls.MaterialButton executeButton;
        private ReaLTaiizor.Controls.MaterialButton clearButton;
        private System.Windows.Forms.FlowLayoutPanel flowLayoutPanel1;
        private System.Windows.Forms.Panel panel1;
        private core.classes.RoundedPanel roundedPanel1;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel1;
        private core.classes.RoundedPanel roundedPanel2;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel2;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel3;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel5;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel6;
        private core.classes.RJTextBox numberOfDeletingColumn;
        private ReaLTaiizor.Controls.MaterialButton createMatrixButton;
        private core.classes.RJTextBox countOfRowsInput;
        private System.Windows.Forms.DataGridView dataGridView;
        private core.classes.RJTextBox countOfColumnsInput;
    }
}