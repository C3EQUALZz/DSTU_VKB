namespace ThirdLaboratory.forms
{
    partial class FormFifthQuestion
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(FormFifthQuestion));
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
            this.panel2 = new System.Windows.Forms.Panel();
            this.roundedPanel3 = new ThirdLaboratory.core.classes.RoundedPanel();
            this.resultListBox = new System.Windows.Forms.ListBox();
            this.dataGridView = new System.Windows.Forms.DataGridView();
            this.Owner = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.Brand = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.Number = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.Year = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.flowLayoutPanel1.SuspendLayout();
            this.panel1.SuspendLayout();
            this.roundedPanel1.SuspendLayout();
            this.tableLayoutPanel1.SuspendLayout();
            this.roundedPanel2.SuspendLayout();
            this.tableLayoutPanel2.SuspendLayout();
            this.panel2.SuspendLayout();
            this.roundedPanel3.SuspendLayout();
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
            this.label1.Text = "Вариант 5";
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
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 36.62149F));
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 63.37851F));
            this.tableLayoutPanel1.Size = new System.Drawing.Size(709, 419);
            this.tableLayoutPanel1.TabIndex = 4;
            // 
            // roundedPanel2
            // 
            this.roundedPanel2.Controls.Add(this.label2);
            this.roundedPanel2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.roundedPanel2.Location = new System.Drawing.Point(4, 17);
            this.roundedPanel2.Margin = new System.Windows.Forms.Padding(4, 17, 4, 4);
            this.roundedPanel2.Name = "roundedPanel2";
            this.roundedPanel2.Size = new System.Drawing.Size(701, 132);
            this.roundedPanel2.TabIndex = 0;
            // 
            // label2
            // 
            this.label2.BackColor = System.Drawing.Color.Transparent;
            this.label2.CausesValidation = false;
            this.label2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.label2.Location = new System.Drawing.Point(0, 0);
            this.label2.Name = "label2";
            this.label2.Padding = new System.Windows.Forms.Padding(20, 18, 20, 18);
            this.label2.Size = new System.Drawing.Size(701, 132);
            this.label2.TabIndex = 0;
            this.label2.Text = resources.GetString("label2.Text");
            // 
            // tableLayoutPanel2
            // 
            this.tableLayoutPanel2.ColumnCount = 1;
            this.tableLayoutPanel2.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanel2.Controls.Add(this.panel2, 0, 1);
            this.tableLayoutPanel2.Controls.Add(this.dataGridView, 0, 0);
            this.tableLayoutPanel2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel2.Location = new System.Drawing.Point(3, 156);
            this.tableLayoutPanel2.Name = "tableLayoutPanel2";
            this.tableLayoutPanel2.RowCount = 2;
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 55.38462F));
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 44.61538F));
            this.tableLayoutPanel2.Size = new System.Drawing.Size(703, 260);
            this.tableLayoutPanel2.TabIndex = 1;
            // 
            // panel2
            // 
            this.panel2.Controls.Add(this.roundedPanel3);
            this.panel2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.panel2.Location = new System.Drawing.Point(3, 147);
            this.panel2.Name = "panel2";
            this.panel2.Size = new System.Drawing.Size(697, 110);
            this.panel2.TabIndex = 0;
            // 
            // roundedPanel3
            // 
            this.roundedPanel3.Controls.Add(this.resultListBox);
            this.roundedPanel3.Dock = System.Windows.Forms.DockStyle.Fill;
            this.roundedPanel3.Location = new System.Drawing.Point(0, 0);
            this.roundedPanel3.Name = "roundedPanel3";
            this.roundedPanel3.Padding = new System.Windows.Forms.Padding(15);
            this.roundedPanel3.Size = new System.Drawing.Size(697, 110);
            this.roundedPanel3.TabIndex = 0;
            // 
            // resultListBox
            // 
            this.resultListBox.Dock = System.Windows.Forms.DockStyle.Fill;
            this.resultListBox.FormattingEnabled = true;
            this.resultListBox.ItemHeight = 16;
            this.resultListBox.Location = new System.Drawing.Point(15, 15);
            this.resultListBox.Name = "resultListBox";
            this.resultListBox.Size = new System.Drawing.Size(667, 80);
            this.resultListBox.TabIndex = 0;
            // 
            // dataGridView
            // 
            this.dataGridView.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridView.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.Owner,
            this.Brand,
            this.Number,
            this.Year});
            this.dataGridView.Dock = System.Windows.Forms.DockStyle.Fill;
            this.dataGridView.Location = new System.Drawing.Point(3, 3);
            this.dataGridView.Name = "dataGridView";
            this.dataGridView.RowHeadersWidth = 51;
            this.dataGridView.RowTemplate.Height = 24;
            this.dataGridView.Size = new System.Drawing.Size(697, 138);
            this.dataGridView.TabIndex = 1;
            this.dataGridView.CellValidating += new System.Windows.Forms.DataGridViewCellValidatingEventHandler(this.DataGridView_CellValidating);
            // 
            // Owner
            // 
            this.Owner.HeaderText = "Владелец";
            this.Owner.MinimumWidth = 6;
            this.Owner.Name = "Owner";
            this.Owner.Width = 125;
            // 
            // Brand
            // 
            this.Brand.HeaderText = "Марка";
            this.Brand.MinimumWidth = 6;
            this.Brand.Name = "Brand";
            this.Brand.Width = 125;
            // 
            // Number
            // 
            this.Number.HeaderText = "Номер";
            this.Number.MinimumWidth = 6;
            this.Number.Name = "Number";
            this.Number.Width = 125;
            // 
            // Year
            // 
            this.Year.HeaderText = "Год выпуска";
            this.Year.MinimumWidth = 6;
            this.Year.Name = "Year";
            this.Year.Width = 125;
            // 
            // FormFifthQuestion
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(709, 558);
            this.Controls.Add(this.tableLayoutPanel1);
            this.Controls.Add(this.panel1);
            this.Controls.Add(this.flowLayoutPanel1);
            this.DoubleBuffered = true;
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.None;
            this.Name = "FormFifthQuestion";
            this.Text = "FormFifthQuestion";
            this.flowLayoutPanel1.ResumeLayout(false);
            this.flowLayoutPanel1.PerformLayout();
            this.panel1.ResumeLayout(false);
            this.roundedPanel1.ResumeLayout(false);
            this.tableLayoutPanel1.ResumeLayout(false);
            this.roundedPanel2.ResumeLayout(false);
            this.tableLayoutPanel2.ResumeLayout(false);
            this.panel2.ResumeLayout(false);
            this.roundedPanel3.ResumeLayout(false);
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
        private System.Windows.Forms.Panel panel2;
        private core.classes.RoundedPanel roundedPanel3;
        private System.Windows.Forms.DataGridView dataGridView;
        private System.Windows.Forms.ListBox resultListBox;
        private System.Windows.Forms.DataGridViewTextBoxColumn Owner;
        private System.Windows.Forms.DataGridViewTextBoxColumn Brand;
        private System.Windows.Forms.DataGridViewTextBoxColumn Number;
        private System.Windows.Forms.DataGridViewTextBoxColumn Year;
    }
}