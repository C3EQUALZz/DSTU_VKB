namespace ThirdLaboratory.forms
{
    partial class FormNinthQuestion
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
            this.clearButton = new ReaLTaiizor.Controls.MaterialButton();
            this.executeButton = new ReaLTaiizor.Controls.MaterialButton();
            this.flowLayoutPanel1 = new System.Windows.Forms.FlowLayoutPanel();
            this.panel1 = new System.Windows.Forms.Panel();
            this.roundedPanel1 = new ThirdLaboratory.core.classes.RoundedPanel();
            this.label1 = new System.Windows.Forms.Label();
            this.panel2 = new System.Windows.Forms.Panel();
            this.tableLayoutPanel1 = new System.Windows.Forms.TableLayoutPanel();
            this.roundedPanel2 = new ThirdLaboratory.core.classes.RoundedPanel();
            this.label2 = new System.Windows.Forms.Label();
            this.tableLayoutPanel2 = new System.Windows.Forms.TableLayoutPanel();
            this.roundedPanel3 = new ThirdLaboratory.core.classes.RoundedPanel();
            this.tableLayoutPanel3 = new System.Windows.Forms.TableLayoutPanel();
            this.panelWithInputLineForN = new System.Windows.Forms.Panel();
            this.countOfMatrixColumnsTextBox = new ThirdLaboratory.core.classes.RJTextBox();
            this.panelWithInputLineForM = new System.Windows.Forms.Panel();
            this.countOfMatrixRowsTextBox = new ThirdLaboratory.core.classes.RJTextBox();
            this.panelForButtonCreateMatrix = new System.Windows.Forms.Panel();
            this.createMatrixButton = new ReaLTaiizor.Controls.MaterialButton();
            this.roundedPanel4 = new ThirdLaboratory.core.classes.RoundedPanel();
            this.dataGridView = new System.Windows.Forms.DataGridView();
            this.flowLayoutPanel1.SuspendLayout();
            this.panel1.SuspendLayout();
            this.roundedPanel1.SuspendLayout();
            this.panel2.SuspendLayout();
            this.tableLayoutPanel1.SuspendLayout();
            this.roundedPanel2.SuspendLayout();
            this.tableLayoutPanel2.SuspendLayout();
            this.roundedPanel3.SuspendLayout();
            this.tableLayoutPanel3.SuspendLayout();
            this.panelWithInputLineForN.SuspendLayout();
            this.panelWithInputLineForM.SuspendLayout();
            this.panelForButtonCreateMatrix.SuspendLayout();
            this.roundedPanel4.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView)).BeginInit();
            this.SuspendLayout();
            // 
            // clearButton
            // 
            this.clearButton.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.clearButton.Density = ReaLTaiizor.Controls.MaterialButton.MaterialButtonDensity.Default;
            this.clearButton.Depth = 0;
            this.clearButton.HighEmphasis = true;
            this.clearButton.Icon = null;
            this.clearButton.IconType = ReaLTaiizor.Controls.MaterialButton.MaterialIconType.Rebase;
            this.clearButton.Location = new System.Drawing.Point(447, 6);
            this.clearButton.Margin = new System.Windows.Forms.Padding(4, 6, 4, 6);
            this.clearButton.MouseState = ReaLTaiizor.Helper.MaterialDrawHelper.MaterialMouseState.HOVER;
            this.clearButton.Name = "clearButton";
            this.clearButton.NoAccentTextColor = System.Drawing.Color.Empty;
            this.clearButton.Size = new System.Drawing.Size(99, 36);
            this.clearButton.TabIndex = 0;
            this.clearButton.Text = "Очистить";
            this.clearButton.Type = ReaLTaiizor.Controls.MaterialButton.MaterialButtonType.Contained;
            this.clearButton.UseAccentColor = false;
            this.clearButton.UseVisualStyleBackColor = true;
            // 
            // executeButton
            // 
            this.executeButton.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.executeButton.Density = ReaLTaiizor.Controls.MaterialButton.MaterialButtonDensity.Default;
            this.executeButton.Depth = 0;
            this.executeButton.HighEmphasis = true;
            this.executeButton.Icon = null;
            this.executeButton.IconType = ReaLTaiizor.Controls.MaterialButton.MaterialIconType.Rebase;
            this.executeButton.Location = new System.Drawing.Point(554, 6);
            this.executeButton.Margin = new System.Windows.Forms.Padding(4, 6, 4, 6);
            this.executeButton.MouseState = ReaLTaiizor.Helper.MaterialDrawHelper.MaterialMouseState.HOVER;
            this.executeButton.Name = "executeButton";
            this.executeButton.NoAccentTextColor = System.Drawing.Color.Empty;
            this.executeButton.Size = new System.Drawing.Size(107, 36);
            this.executeButton.TabIndex = 1;
            this.executeButton.Text = "Запустить";
            this.executeButton.Type = ReaLTaiizor.Controls.MaterialButton.MaterialButtonType.Contained;
            this.executeButton.UseAccentColor = false;
            this.executeButton.UseVisualStyleBackColor = true;
            this.executeButton.Click += new System.EventHandler(this.ExecuteButton_Click);
            // 
            // flowLayoutPanel1
            // 
            this.flowLayoutPanel1.AutoSize = true;
            this.flowLayoutPanel1.Controls.Add(this.executeButton);
            this.flowLayoutPanel1.Controls.Add(this.clearButton);
            this.flowLayoutPanel1.Dock = System.Windows.Forms.DockStyle.Bottom;
            this.flowLayoutPanel1.FlowDirection = System.Windows.Forms.FlowDirection.RightToLeft;
            this.flowLayoutPanel1.Location = new System.Drawing.Point(0, 518);
            this.flowLayoutPanel1.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.flowLayoutPanel1.Name = "flowLayoutPanel1";
            this.flowLayoutPanel1.Size = new System.Drawing.Size(665, 48);
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
            this.panel1.Size = new System.Drawing.Size(665, 93);
            this.panel1.TabIndex = 3;
            // 
            // roundedPanel1
            // 
            this.roundedPanel1.Controls.Add(this.label1);
            this.roundedPanel1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.roundedPanel1.Location = new System.Drawing.Point(5, 5);
            this.roundedPanel1.Name = "roundedPanel1";
            this.roundedPanel1.Size = new System.Drawing.Size(655, 88);
            this.roundedPanel1.TabIndex = 0;
            // 
            // label1
            // 
            this.label1.BackColor = System.Drawing.Color.Transparent;
            this.label1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.label1.Font = new System.Drawing.Font("MS Reference Sans Serif", 24F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.Location = new System.Drawing.Point(0, 0);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(655, 88);
            this.label1.TabIndex = 0;
            this.label1.Text = "Вариант 9";
            this.label1.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // panel2
            // 
            this.panel2.Controls.Add(this.tableLayoutPanel1);
            this.panel2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.panel2.Location = new System.Drawing.Point(0, 93);
            this.panel2.Name = "panel2";
            this.panel2.Size = new System.Drawing.Size(665, 425);
            this.panel2.TabIndex = 4;
            // 
            // tableLayoutPanel1
            // 
            this.tableLayoutPanel1.ColumnCount = 1;
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.tableLayoutPanel1.Controls.Add(this.roundedPanel2, 0, 0);
            this.tableLayoutPanel1.Controls.Add(this.tableLayoutPanel2, 0, 1);
            this.tableLayoutPanel1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel1.Location = new System.Drawing.Point(0, 0);
            this.tableLayoutPanel1.Name = "tableLayoutPanel1";
            this.tableLayoutPanel1.RowCount = 2;
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 32.57F));
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 67.43F));
            this.tableLayoutPanel1.Size = new System.Drawing.Size(665, 425);
            this.tableLayoutPanel1.TabIndex = 0;
            // 
            // roundedPanel2
            // 
            this.roundedPanel2.Controls.Add(this.label2);
            this.roundedPanel2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.roundedPanel2.Location = new System.Drawing.Point(4, 18);
            this.roundedPanel2.Margin = new System.Windows.Forms.Padding(4, 18, 4, 4);
            this.roundedPanel2.Name = "roundedPanel2";
            this.roundedPanel2.Size = new System.Drawing.Size(657, 116);
            this.roundedPanel2.TabIndex = 0;
            // 
            // label2
            // 
            this.label2.BackColor = System.Drawing.Color.Transparent;
            this.label2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.label2.Font = new System.Drawing.Font("Segoe UI", 7.8F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label2.Location = new System.Drawing.Point(0, 0);
            this.label2.Name = "label2";
            this.label2.Padding = new System.Windows.Forms.Padding(20, 18, 20, 18);
            this.label2.Size = new System.Drawing.Size(657, 116);
            this.label2.TabIndex = 0;
            this.label2.Text = "Дана матрица размера M × N. Поменять местами столбец с номером N и последний из с" +
    "толбцов, содержащих только положительные элементы. Если требуемых столбцов нет, " +
    "то вывести матрицу без изменений.";
            // 
            // tableLayoutPanel2
            // 
            this.tableLayoutPanel2.ColumnCount = 1;
            this.tableLayoutPanel2.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.tableLayoutPanel2.Controls.Add(this.roundedPanel3, 0, 0);
            this.tableLayoutPanel2.Controls.Add(this.roundedPanel4, 0, 1);
            this.tableLayoutPanel2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel2.Location = new System.Drawing.Point(3, 141);
            this.tableLayoutPanel2.Name = "tableLayoutPanel2";
            this.tableLayoutPanel2.RowCount = 2;
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 28.57143F));
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 71.42857F));
            this.tableLayoutPanel2.Size = new System.Drawing.Size(659, 281);
            this.tableLayoutPanel2.TabIndex = 1;
            // 
            // roundedPanel3
            // 
            this.roundedPanel3.Controls.Add(this.tableLayoutPanel3);
            this.roundedPanel3.Dock = System.Windows.Forms.DockStyle.Fill;
            this.roundedPanel3.Location = new System.Drawing.Point(3, 3);
            this.roundedPanel3.Name = "roundedPanel3";
            this.roundedPanel3.Size = new System.Drawing.Size(653, 74);
            this.roundedPanel3.TabIndex = 0;
            // 
            // tableLayoutPanel3
            // 
            this.tableLayoutPanel3.BackColor = System.Drawing.Color.Transparent;
            this.tableLayoutPanel3.ColumnCount = 3;
            this.tableLayoutPanel3.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33.33333F));
            this.tableLayoutPanel3.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33.33333F));
            this.tableLayoutPanel3.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33.33333F));
            this.tableLayoutPanel3.Controls.Add(this.panelWithInputLineForN, 1, 0);
            this.tableLayoutPanel3.Controls.Add(this.panelWithInputLineForM, 0, 0);
            this.tableLayoutPanel3.Controls.Add(this.panelForButtonCreateMatrix, 2, 0);
            this.tableLayoutPanel3.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel3.Location = new System.Drawing.Point(0, 0);
            this.tableLayoutPanel3.Name = "tableLayoutPanel3";
            this.tableLayoutPanel3.RowCount = 1;
            this.tableLayoutPanel3.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.tableLayoutPanel3.Size = new System.Drawing.Size(653, 74);
            this.tableLayoutPanel3.TabIndex = 0;
            // 
            // panelWithInputLineForN
            // 
            this.panelWithInputLineForN.Controls.Add(this.countOfMatrixColumnsTextBox);
            this.panelWithInputLineForN.Dock = System.Windows.Forms.DockStyle.Fill;
            this.panelWithInputLineForN.Location = new System.Drawing.Point(220, 3);
            this.panelWithInputLineForN.Name = "panelWithInputLineForN";
            this.panelWithInputLineForN.Padding = new System.Windows.Forms.Padding(10, 15, 10, 15);
            this.panelWithInputLineForN.Size = new System.Drawing.Size(211, 68);
            this.panelWithInputLineForN.TabIndex = 0;
            // 
            // countOfMatrixColumnsTextBox
            // 
            this.countOfMatrixColumnsTextBox.BackColor = System.Drawing.SystemColors.Window;
            this.countOfMatrixColumnsTextBox.BorderColor = System.Drawing.Color.MediumSlateBlue;
            this.countOfMatrixColumnsTextBox.BorderFocusColor = System.Drawing.Color.HotPink;
            this.countOfMatrixColumnsTextBox.BorderRadius = 10;
            this.countOfMatrixColumnsTextBox.BorderSize = 2;
            this.countOfMatrixColumnsTextBox.Dock = System.Windows.Forms.DockStyle.Fill;
            this.countOfMatrixColumnsTextBox.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.countOfMatrixColumnsTextBox.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(64)))), ((int)(((byte)(64)))), ((int)(((byte)(64)))));
            this.countOfMatrixColumnsTextBox.Location = new System.Drawing.Point(10, 15);
            this.countOfMatrixColumnsTextBox.Margin = new System.Windows.Forms.Padding(10, 4, 4, 4);
            this.countOfMatrixColumnsTextBox.Multiline = false;
            this.countOfMatrixColumnsTextBox.Name = "countOfMatrixColumnsTextBox";
            this.countOfMatrixColumnsTextBox.Padding = new System.Windows.Forms.Padding(10, 7, 10, 7);
            this.countOfMatrixColumnsTextBox.PasswordChar = false;
            this.countOfMatrixColumnsTextBox.PlaceholderColor = System.Drawing.Color.DarkGray;
            this.countOfMatrixColumnsTextBox.PlaceholderText = "Кол-во столбцов (N)";
            this.countOfMatrixColumnsTextBox.Size = new System.Drawing.Size(191, 35);
            this.countOfMatrixColumnsTextBox.TabIndex = 0;
            this.countOfMatrixColumnsTextBox.Texts = "";
            this.countOfMatrixColumnsTextBox.UnderlinedStyle = false;
            this.countOfMatrixColumnsTextBox._TextChanged += new System.EventHandler(this.CountOfMatrixColumnsTextBox__TextChanged);
            // 
            // panelWithInputLineForM
            // 
            this.panelWithInputLineForM.Controls.Add(this.countOfMatrixRowsTextBox);
            this.panelWithInputLineForM.Dock = System.Windows.Forms.DockStyle.Fill;
            this.panelWithInputLineForM.Location = new System.Drawing.Point(3, 3);
            this.panelWithInputLineForM.Name = "panelWithInputLineForM";
            this.panelWithInputLineForM.Padding = new System.Windows.Forms.Padding(10, 15, 10, 15);
            this.panelWithInputLineForM.Size = new System.Drawing.Size(211, 68);
            this.panelWithInputLineForM.TabIndex = 1;
            // 
            // countOfMatrixRowsTextBox
            // 
            this.countOfMatrixRowsTextBox.BackColor = System.Drawing.SystemColors.Window;
            this.countOfMatrixRowsTextBox.BorderColor = System.Drawing.Color.MediumSlateBlue;
            this.countOfMatrixRowsTextBox.BorderFocusColor = System.Drawing.Color.HotPink;
            this.countOfMatrixRowsTextBox.BorderRadius = 10;
            this.countOfMatrixRowsTextBox.BorderSize = 2;
            this.countOfMatrixRowsTextBox.Dock = System.Windows.Forms.DockStyle.Fill;
            this.countOfMatrixRowsTextBox.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.countOfMatrixRowsTextBox.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(64)))), ((int)(((byte)(64)))), ((int)(((byte)(64)))));
            this.countOfMatrixRowsTextBox.Location = new System.Drawing.Point(10, 15);
            this.countOfMatrixRowsTextBox.Margin = new System.Windows.Forms.Padding(10, 4, 4, 4);
            this.countOfMatrixRowsTextBox.Multiline = false;
            this.countOfMatrixRowsTextBox.Name = "countOfMatrixRowsTextBox";
            this.countOfMatrixRowsTextBox.Padding = new System.Windows.Forms.Padding(10, 7, 10, 7);
            this.countOfMatrixRowsTextBox.PasswordChar = false;
            this.countOfMatrixRowsTextBox.PlaceholderColor = System.Drawing.Color.DarkGray;
            this.countOfMatrixRowsTextBox.PlaceholderText = "Кол-во строк (M)";
            this.countOfMatrixRowsTextBox.Size = new System.Drawing.Size(191, 35);
            this.countOfMatrixRowsTextBox.TabIndex = 0;
            this.countOfMatrixRowsTextBox.Texts = "";
            this.countOfMatrixRowsTextBox.UnderlinedStyle = false;
            this.countOfMatrixRowsTextBox._TextChanged += new System.EventHandler(this.CountOfMatrixRowsTextBox__TextChanged);
            // 
            // panelForButtonCreateMatrix
            // 
            this.panelForButtonCreateMatrix.Controls.Add(this.createMatrixButton);
            this.panelForButtonCreateMatrix.Dock = System.Windows.Forms.DockStyle.Fill;
            this.panelForButtonCreateMatrix.Location = new System.Drawing.Point(437, 3);
            this.panelForButtonCreateMatrix.Name = "panelForButtonCreateMatrix";
            this.panelForButtonCreateMatrix.Padding = new System.Windows.Forms.Padding(10, 15, 10, 15);
            this.panelForButtonCreateMatrix.Size = new System.Drawing.Size(213, 68);
            this.panelForButtonCreateMatrix.TabIndex = 2;
            // 
            // createMatrixButton
            // 
            this.createMatrixButton.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.createMatrixButton.Density = ReaLTaiizor.Controls.MaterialButton.MaterialButtonDensity.Default;
            this.createMatrixButton.Depth = 0;
            this.createMatrixButton.Dock = System.Windows.Forms.DockStyle.Fill;
            this.createMatrixButton.HighEmphasis = true;
            this.createMatrixButton.Icon = null;
            this.createMatrixButton.IconType = ReaLTaiizor.Controls.MaterialButton.MaterialIconType.Rebase;
            this.createMatrixButton.Location = new System.Drawing.Point(10, 15);
            this.createMatrixButton.Margin = new System.Windows.Forms.Padding(4, 6, 4, 6);
            this.createMatrixButton.MouseState = ReaLTaiizor.Helper.MaterialDrawHelper.MaterialMouseState.HOVER;
            this.createMatrixButton.Name = "createMatrixButton";
            this.createMatrixButton.NoAccentTextColor = System.Drawing.Color.Empty;
            this.createMatrixButton.Size = new System.Drawing.Size(193, 38);
            this.createMatrixButton.TabIndex = 0;
            this.createMatrixButton.Text = "Создать матрицу";
            this.createMatrixButton.Type = ReaLTaiizor.Controls.MaterialButton.MaterialButtonType.Contained;
            this.createMatrixButton.UseAccentColor = false;
            this.createMatrixButton.UseVisualStyleBackColor = true;
            this.createMatrixButton.Click += new System.EventHandler(this.CreateMatrixButton_Click);
            // 
            // roundedPanel4
            // 
            this.roundedPanel4.Controls.Add(this.dataGridView);
            this.roundedPanel4.Dock = System.Windows.Forms.DockStyle.Fill;
            this.roundedPanel4.Location = new System.Drawing.Point(3, 83);
            this.roundedPanel4.Name = "roundedPanel4";
            this.roundedPanel4.Padding = new System.Windows.Forms.Padding(15);
            this.roundedPanel4.Size = new System.Drawing.Size(653, 195);
            this.roundedPanel4.TabIndex = 1;
            // 
            // dataGridView
            // 
            this.dataGridView.AllowUserToAddRows = false;
            this.dataGridView.AllowUserToDeleteRows = false;
            this.dataGridView.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridView.Dock = System.Windows.Forms.DockStyle.Fill;
            this.dataGridView.Location = new System.Drawing.Point(15, 15);
            this.dataGridView.Name = "dataGridView";
            this.dataGridView.RowHeadersWidth = 51;
            this.dataGridView.RowTemplate.Height = 24;
            this.dataGridView.Size = new System.Drawing.Size(623, 165);
            this.dataGridView.TabIndex = 0;
            // 
            // FormNinthQuestion
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(665, 566);
            this.Controls.Add(this.panel2);
            this.Controls.Add(this.panel1);
            this.Controls.Add(this.flowLayoutPanel1);
            this.DoubleBuffered = true;
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.None;
            this.Name = "FormNinthQuestion";
            this.Text = "FormNinthQuestion";
            this.flowLayoutPanel1.ResumeLayout(false);
            this.flowLayoutPanel1.PerformLayout();
            this.panel1.ResumeLayout(false);
            this.roundedPanel1.ResumeLayout(false);
            this.panel2.ResumeLayout(false);
            this.tableLayoutPanel1.ResumeLayout(false);
            this.roundedPanel2.ResumeLayout(false);
            this.tableLayoutPanel2.ResumeLayout(false);
            this.roundedPanel3.ResumeLayout(false);
            this.tableLayoutPanel3.ResumeLayout(false);
            this.panelWithInputLineForN.ResumeLayout(false);
            this.panelWithInputLineForM.ResumeLayout(false);
            this.panelForButtonCreateMatrix.ResumeLayout(false);
            this.panelForButtonCreateMatrix.PerformLayout();
            this.roundedPanel4.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private ReaLTaiizor.Controls.MaterialButton clearButton;
        private ReaLTaiizor.Controls.MaterialButton executeButton;
        private System.Windows.Forms.FlowLayoutPanel flowLayoutPanel1;
        private System.Windows.Forms.Panel panel1;
        private core.classes.RoundedPanel roundedPanel1;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Panel panel2;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel1;
        private core.classes.RoundedPanel roundedPanel2;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel2;
        private core.classes.RoundedPanel roundedPanel3;
        private core.classes.RoundedPanel roundedPanel4;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel3;
        private System.Windows.Forms.Panel panelWithInputLineForN;
        private core.classes.RJTextBox countOfMatrixColumnsTextBox;
        private System.Windows.Forms.Panel panelWithInputLineForM;
        private core.classes.RJTextBox countOfMatrixRowsTextBox;
        private System.Windows.Forms.Panel panelForButtonCreateMatrix;
        private ReaLTaiizor.Controls.MaterialButton createMatrixButton;
        private System.Windows.Forms.DataGridView dataGridView;
    }
}