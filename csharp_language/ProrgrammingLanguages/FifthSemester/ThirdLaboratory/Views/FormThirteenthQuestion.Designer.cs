namespace ThirdLaboratory.forms
{
    partial class FormThirteenthQuestion
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
            this.roundedPanel3 = new ThirdLaboratory.core.classes.RoundedPanel();
            this.outputLabel = new System.Windows.Forms.Label();
            this.tableLayoutPanel3 = new System.Windows.Forms.TableLayoutPanel();
            this.dataGridView = new System.Windows.Forms.DataGridView();
            this.tableLayoutPanel4 = new System.Windows.Forms.TableLayoutPanel();
            this.iconMenuItem1 = new FontAwesome.Sharp.IconMenuItem();
            this.iconMenuItem2 = new FontAwesome.Sharp.IconMenuItem();
            this.tableLayoutPanel5 = new System.Windows.Forms.TableLayoutPanel();
            this.countOfRows = new ThirdLaboratory.core.classes.RJTextBox();
            this.countOfColumns = new ThirdLaboratory.core.classes.RJTextBox();
            this.numberOfRow = new ThirdLaboratory.core.classes.RJTextBox();
            this.iconMenuItem3 = new FontAwesome.Sharp.IconMenuItem();
            this.generateRandomMatrixButton = new ReaLTaiizor.Controls.MaterialButton();
            this.flowLayoutPanel1.SuspendLayout();
            this.panel1.SuspendLayout();
            this.roundedPanel1.SuspendLayout();
            this.tableLayoutPanel1.SuspendLayout();
            this.roundedPanel2.SuspendLayout();
            this.tableLayoutPanel2.SuspendLayout();
            this.roundedPanel3.SuspendLayout();
            this.tableLayoutPanel3.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView)).BeginInit();
            this.tableLayoutPanel4.SuspendLayout();
            this.tableLayoutPanel5.SuspendLayout();
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
            this.flowLayoutPanel1.WrapContents = false;
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
            this.label1.Text = "Вариант 13";
            this.label1.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // tableLayoutPanel1
            // 
            this.tableLayoutPanel1.ColumnCount = 1;
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.tableLayoutPanel1.Controls.Add(this.roundedPanel2, 0, 0);
            this.tableLayoutPanel1.Controls.Add(this.tableLayoutPanel2, 0, 1);
            this.tableLayoutPanel1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel1.Location = new System.Drawing.Point(0, 91);
            this.tableLayoutPanel1.Name = "tableLayoutPanel1";
            this.tableLayoutPanel1.RowCount = 2;
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 27.10904F));
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 72.89096F));
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
            this.roundedPanel2.Size = new System.Drawing.Size(703, 96);
            this.roundedPanel2.TabIndex = 0;
            // 
            // label2
            // 
            this.label2.BackColor = System.Drawing.Color.Transparent;
            this.label2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.label2.Location = new System.Drawing.Point(0, 0);
            this.label2.Name = "label2";
            this.label2.Padding = new System.Windows.Forms.Padding(18, 20, 18, 20);
            this.label2.Size = new System.Drawing.Size(703, 96);
            this.label2.TabIndex = 0;
            this.label2.Text = "Заполнить матрицу случайными числами размера M × N и целое число K(1 ≤ K ≤ M). Вы" +
    "вести элементы K-й строки данной матрицы. Обеспечьте контроль вводимых значений." +
    " Обеспечьте контроль вводимых значений.";
            // 
            // tableLayoutPanel2
            // 
            this.tableLayoutPanel2.ColumnCount = 1;
            this.tableLayoutPanel2.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.tableLayoutPanel2.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 20F));
            this.tableLayoutPanel2.Controls.Add(this.roundedPanel3, 0, 1);
            this.tableLayoutPanel2.Controls.Add(this.tableLayoutPanel3, 0, 0);
            this.tableLayoutPanel2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel2.Location = new System.Drawing.Point(3, 116);
            this.tableLayoutPanel2.Name = "tableLayoutPanel2";
            this.tableLayoutPanel2.RowCount = 2;
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 62F));
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 38F));
            this.tableLayoutPanel2.Size = new System.Drawing.Size(703, 300);
            this.tableLayoutPanel2.TabIndex = 1;
            // 
            // roundedPanel3
            // 
            this.roundedPanel3.Controls.Add(this.outputLabel);
            this.roundedPanel3.Dock = System.Windows.Forms.DockStyle.Fill;
            this.roundedPanel3.Location = new System.Drawing.Point(3, 189);
            this.roundedPanel3.Name = "roundedPanel3";
            this.roundedPanel3.Size = new System.Drawing.Size(697, 108);
            this.roundedPanel3.TabIndex = 0;
            // 
            // outputLabel
            // 
            this.outputLabel.BackColor = System.Drawing.Color.Transparent;
            this.outputLabel.Dock = System.Windows.Forms.DockStyle.Fill;
            this.outputLabel.Location = new System.Drawing.Point(0, 0);
            this.outputLabel.Name = "outputLabel";
            this.outputLabel.Padding = new System.Windows.Forms.Padding(15, 15, 0, 0);
            this.outputLabel.Size = new System.Drawing.Size(697, 108);
            this.outputLabel.TabIndex = 0;
            // 
            // tableLayoutPanel3
            // 
            this.tableLayoutPanel3.ColumnCount = 2;
            this.tableLayoutPanel3.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 56.95839F));
            this.tableLayoutPanel3.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 43.04161F));
            this.tableLayoutPanel3.Controls.Add(this.dataGridView, 0, 0);
            this.tableLayoutPanel3.Controls.Add(this.tableLayoutPanel4, 1, 0);
            this.tableLayoutPanel3.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel3.Location = new System.Drawing.Point(3, 3);
            this.tableLayoutPanel3.Name = "tableLayoutPanel3";
            this.tableLayoutPanel3.RowCount = 1;
            this.tableLayoutPanel3.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanel3.Size = new System.Drawing.Size(697, 180);
            this.tableLayoutPanel3.TabIndex = 1;
            // 
            // dataGridView
            // 
            this.dataGridView.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridView.Dock = System.Windows.Forms.DockStyle.Fill;
            this.dataGridView.Location = new System.Drawing.Point(3, 3);
            this.dataGridView.Name = "dataGridView";
            this.dataGridView.RowHeadersWidth = 51;
            this.dataGridView.RowTemplate.Height = 24;
            this.dataGridView.Size = new System.Drawing.Size(391, 174);
            this.dataGridView.TabIndex = 0;
            // 
            // tableLayoutPanel4
            // 
            this.tableLayoutPanel4.ColumnCount = 1;
            this.tableLayoutPanel4.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanel4.Controls.Add(this.generateRandomMatrixButton, 0, 1);
            this.tableLayoutPanel4.Controls.Add(this.tableLayoutPanel5, 0, 0);
            this.tableLayoutPanel4.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel4.Location = new System.Drawing.Point(400, 3);
            this.tableLayoutPanel4.Name = "tableLayoutPanel4";
            this.tableLayoutPanel4.RowCount = 2;
            this.tableLayoutPanel4.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 63.7931F));
            this.tableLayoutPanel4.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 36.2069F));
            this.tableLayoutPanel4.Size = new System.Drawing.Size(294, 174);
            this.tableLayoutPanel4.TabIndex = 1;
            // 
            // iconMenuItem1
            // 
            this.iconMenuItem1.IconChar = FontAwesome.Sharp.IconChar.None;
            this.iconMenuItem1.IconColor = System.Drawing.Color.Black;
            this.iconMenuItem1.IconFont = FontAwesome.Sharp.IconFont.Auto;
            this.iconMenuItem1.Name = "iconMenuItem1";
            this.iconMenuItem1.Size = new System.Drawing.Size(32, 19);
            this.iconMenuItem1.Text = "iconMenuItem1";
            // 
            // iconMenuItem2
            // 
            this.iconMenuItem2.IconChar = FontAwesome.Sharp.IconChar.None;
            this.iconMenuItem2.IconColor = System.Drawing.Color.Black;
            this.iconMenuItem2.IconFont = FontAwesome.Sharp.IconFont.Auto;
            this.iconMenuItem2.Name = "iconMenuItem2";
            this.iconMenuItem2.Size = new System.Drawing.Size(32, 19);
            this.iconMenuItem2.Text = "iconMenuItem2";
            // 
            // tableLayoutPanel5
            // 
            this.tableLayoutPanel5.ColumnCount = 3;
            this.tableLayoutPanel5.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33.33333F));
            this.tableLayoutPanel5.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33.33333F));
            this.tableLayoutPanel5.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33.33333F));
            this.tableLayoutPanel5.Controls.Add(this.countOfRows, 0, 0);
            this.tableLayoutPanel5.Controls.Add(this.countOfColumns, 1, 0);
            this.tableLayoutPanel5.Controls.Add(this.numberOfRow, 2, 0);
            this.tableLayoutPanel5.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel5.Location = new System.Drawing.Point(3, 3);
            this.tableLayoutPanel5.Name = "tableLayoutPanel5";
            this.tableLayoutPanel5.RowCount = 1;
            this.tableLayoutPanel5.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.tableLayoutPanel5.Size = new System.Drawing.Size(288, 105);
            this.tableLayoutPanel5.TabIndex = 0;
            // 
            // countOfRows
            // 
            this.countOfRows.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.countOfRows.BackColor = System.Drawing.SystemColors.Window;
            this.countOfRows.BorderColor = System.Drawing.Color.MediumSlateBlue;
            this.countOfRows.BorderFocusColor = System.Drawing.Color.HotPink;
            this.countOfRows.BorderRadius = 0;
            this.countOfRows.BorderSize = 2;
            this.countOfRows.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.countOfRows.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(64)))), ((int)(((byte)(64)))), ((int)(((byte)(64)))));
            this.countOfRows.Location = new System.Drawing.Point(4, 35);
            this.countOfRows.Margin = new System.Windows.Forms.Padding(4);
            this.countOfRows.Multiline = false;
            this.countOfRows.Name = "countOfRows";
            this.countOfRows.Padding = new System.Windows.Forms.Padding(10, 7, 10, 7);
            this.countOfRows.PasswordChar = false;
            this.countOfRows.PlaceholderColor = System.Drawing.Color.DarkGray;
            this.countOfRows.PlaceholderText = "M:";
            this.countOfRows.Size = new System.Drawing.Size(88, 35);
            this.countOfRows.TabIndex = 0;
            this.countOfRows.Texts = "";
            this.countOfRows.UnderlinedStyle = false;
            this.countOfRows.Validating += new System.ComponentModel.CancelEventHandler(this.CountOfRows_Validating);
            // 
            // countOfColumns
            // 
            this.countOfColumns.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.countOfColumns.BackColor = System.Drawing.SystemColors.Window;
            this.countOfColumns.BorderColor = System.Drawing.Color.MediumSlateBlue;
            this.countOfColumns.BorderFocusColor = System.Drawing.Color.HotPink;
            this.countOfColumns.BorderRadius = 0;
            this.countOfColumns.BorderSize = 2;
            this.countOfColumns.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.countOfColumns.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(64)))), ((int)(((byte)(64)))), ((int)(((byte)(64)))));
            this.countOfColumns.Location = new System.Drawing.Point(100, 35);
            this.countOfColumns.Margin = new System.Windows.Forms.Padding(4);
            this.countOfColumns.Multiline = false;
            this.countOfColumns.Name = "countOfColumns";
            this.countOfColumns.Padding = new System.Windows.Forms.Padding(10, 7, 10, 7);
            this.countOfColumns.PasswordChar = false;
            this.countOfColumns.PlaceholderColor = System.Drawing.Color.DarkGray;
            this.countOfColumns.PlaceholderText = "N:";
            this.countOfColumns.Size = new System.Drawing.Size(88, 35);
            this.countOfColumns.TabIndex = 1;
            this.countOfColumns.Texts = "";
            this.countOfColumns.UnderlinedStyle = false;
            this.countOfColumns.Validating += new System.ComponentModel.CancelEventHandler(this.CountOfColumns_Validating);
            // 
            // numberOfRow
            // 
            this.numberOfRow.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.numberOfRow.BackColor = System.Drawing.SystemColors.Window;
            this.numberOfRow.BorderColor = System.Drawing.Color.MediumSlateBlue;
            this.numberOfRow.BorderFocusColor = System.Drawing.Color.HotPink;
            this.numberOfRow.BorderRadius = 0;
            this.numberOfRow.BorderSize = 2;
            this.numberOfRow.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.numberOfRow.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(64)))), ((int)(((byte)(64)))), ((int)(((byte)(64)))));
            this.numberOfRow.Location = new System.Drawing.Point(196, 35);
            this.numberOfRow.Margin = new System.Windows.Forms.Padding(4);
            this.numberOfRow.Multiline = false;
            this.numberOfRow.Name = "numberOfRow";
            this.numberOfRow.Padding = new System.Windows.Forms.Padding(10, 7, 10, 7);
            this.numberOfRow.PasswordChar = false;
            this.numberOfRow.PlaceholderColor = System.Drawing.Color.DarkGray;
            this.numberOfRow.PlaceholderText = "K:";
            this.numberOfRow.Size = new System.Drawing.Size(88, 35);
            this.numberOfRow.TabIndex = 2;
            this.numberOfRow.Texts = "";
            this.numberOfRow.UnderlinedStyle = false;
            this.numberOfRow.Validating += new System.ComponentModel.CancelEventHandler(this.NumberOfRow_Validating);
            // 
            // iconMenuItem3
            // 
            this.iconMenuItem3.IconChar = FontAwesome.Sharp.IconChar.None;
            this.iconMenuItem3.IconColor = System.Drawing.Color.Black;
            this.iconMenuItem3.IconFont = FontAwesome.Sharp.IconFont.Auto;
            this.iconMenuItem3.Name = "iconMenuItem3";
            this.iconMenuItem3.Size = new System.Drawing.Size(32, 19);
            this.iconMenuItem3.Text = "iconMenuItem3";
            // 
            // generateRandomMatrixButton
            // 
            this.generateRandomMatrixButton.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.generateRandomMatrixButton.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.generateRandomMatrixButton.Density = ReaLTaiizor.Controls.MaterialButton.MaterialButtonDensity.Default;
            this.generateRandomMatrixButton.Depth = 0;
            this.generateRandomMatrixButton.HighEmphasis = true;
            this.generateRandomMatrixButton.Icon = null;
            this.generateRandomMatrixButton.IconType = ReaLTaiizor.Controls.MaterialButton.MaterialIconType.Rebase;
            this.generateRandomMatrixButton.Location = new System.Drawing.Point(54, 124);
            this.generateRandomMatrixButton.Margin = new System.Windows.Forms.Padding(4, 6, 4, 6);
            this.generateRandomMatrixButton.MouseState = ReaLTaiizor.Helper.MaterialDrawHelper.MaterialMouseState.HOVER;
            this.generateRandomMatrixButton.Name = "generateRandomMatrixButton";
            this.generateRandomMatrixButton.NoAccentTextColor = System.Drawing.Color.Empty;
            this.generateRandomMatrixButton.Size = new System.Drawing.Size(186, 36);
            this.generateRandomMatrixButton.TabIndex = 1;
            this.generateRandomMatrixButton.Text = "Генерация матрицы";
            this.generateRandomMatrixButton.Type = ReaLTaiizor.Controls.MaterialButton.MaterialButtonType.Contained;
            this.generateRandomMatrixButton.UseAccentColor = false;
            this.generateRandomMatrixButton.UseVisualStyleBackColor = true;
            this.generateRandomMatrixButton.Click += new System.EventHandler(this.GenerateRandomMatrixButton_Click);
            // 
            // FormThirteenthQuestion
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(709, 558);
            this.Controls.Add(this.tableLayoutPanel1);
            this.Controls.Add(this.panel1);
            this.Controls.Add(this.flowLayoutPanel1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.None;
            this.Name = "FormThirteenthQuestion";
            this.Text = "FormThirteenthQuestion";
            this.flowLayoutPanel1.ResumeLayout(false);
            this.flowLayoutPanel1.PerformLayout();
            this.panel1.ResumeLayout(false);
            this.roundedPanel1.ResumeLayout(false);
            this.tableLayoutPanel1.ResumeLayout(false);
            this.roundedPanel2.ResumeLayout(false);
            this.tableLayoutPanel2.ResumeLayout(false);
            this.roundedPanel3.ResumeLayout(false);
            this.tableLayoutPanel3.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView)).EndInit();
            this.tableLayoutPanel4.ResumeLayout(false);
            this.tableLayoutPanel4.PerformLayout();
            this.tableLayoutPanel5.ResumeLayout(false);
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
        private core.classes.RoundedPanel roundedPanel3;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel3;
        private System.Windows.Forms.DataGridView dataGridView;
        private FontAwesome.Sharp.IconMenuItem iconMenuItem1;
        private FontAwesome.Sharp.IconMenuItem iconMenuItem2;
        private System.Windows.Forms.Label outputLabel;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel4;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel5;
        private core.classes.RJTextBox countOfRows;
        private core.classes.RJTextBox countOfColumns;
        private core.classes.RJTextBox numberOfRow;
        private ReaLTaiizor.Controls.MaterialButton generateRandomMatrixButton;
        private FontAwesome.Sharp.IconMenuItem iconMenuItem3;
    }
}