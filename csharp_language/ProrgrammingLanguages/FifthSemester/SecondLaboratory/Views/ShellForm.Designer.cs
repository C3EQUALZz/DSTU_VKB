namespace SecondLaboratory
{
    partial class ShellForm
    {
        /// <summary>
        /// Обязательная переменная конструктора.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Освободить все используемые ресурсы.
        /// </summary>
        /// <param name="disposing">истинно, если управляемый ресурс должен быть удален; иначе ложно.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Код, автоматически созданный конструктором форм Windows

        /// <summary>
        /// Требуемый метод для поддержки конструктора — не изменяйте 
        /// содержимое этого метода с помощью редактора кода.
        /// </summary>
        private void InitializeComponent()
        {
            this.panel1 = new System.Windows.Forms.Panel();
            this.NavigationButton = new System.Windows.Forms.Button();
            this.NavigationPanel = new System.Windows.Forms.Panel();
            this.NavigationItemsPanel = new System.Windows.Forms.Panel();
            this.CalculatorContainerPanel = new System.Windows.Forms.Panel();
            this.panel2 = new System.Windows.Forms.Panel();
            this.PageTitleLabel = new System.Windows.Forms.Label();
            this.panel1.SuspendLayout();
            this.NavigationPanel.SuspendLayout();
            this.panel2.SuspendLayout();
            this.SuspendLayout();
            // 
            // panel1
            // 
            this.panel1.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.panel1.Controls.Add(this.NavigationButton);
            this.panel1.Controls.Add(this.NavigationPanel);
            this.panel1.Controls.Add(this.CalculatorContainerPanel);
            this.panel1.Controls.Add(this.panel2);
            this.panel1.Location = new System.Drawing.Point(0, 0);
            this.panel1.Margin = new System.Windows.Forms.Padding(0);
            this.panel1.Name = "panel1";
            this.panel1.Size = new System.Drawing.Size(328, 494);
            this.panel1.TabIndex = 0;
            // 
            // NavigationButton
            // 
            this.NavigationButton.BackColor = System.Drawing.Color.Transparent;
            this.NavigationButton.BackgroundImage = global::SecondLaboratory.Properties.Resources.menu_svgrepo_com;
            this.NavigationButton.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch;
            this.NavigationButton.FlatAppearance.BorderSize = 0;
            this.NavigationButton.FlatAppearance.MouseDownBackColor = System.Drawing.Color.FromArgb(((int)(((byte)(42)))), ((int)(((byte)(42)))), ((int)(((byte)(42)))));
            this.NavigationButton.FlatAppearance.MouseOverBackColor = System.Drawing.Color.FromArgb(((int)(((byte)(42)))), ((int)(((byte)(42)))), ((int)(((byte)(42)))));
            this.NavigationButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.NavigationButton.Location = new System.Drawing.Point(18, 16);
            this.NavigationButton.Margin = new System.Windows.Forms.Padding(0);
            this.NavigationButton.Name = "NavigationButton";
            this.NavigationButton.Padding = new System.Windows.Forms.Padding(5);
            this.NavigationButton.Size = new System.Drawing.Size(20, 20);
            this.NavigationButton.TabIndex = 0;
            this.NavigationButton.TabStop = false;
            this.NavigationButton.UseVisualStyleBackColor = false;
            this.NavigationButton.Click += new System.EventHandler(this.NavigationButton_Click);
            // 
            // NavigationPanel
            // 
            this.NavigationPanel.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.NavigationPanel.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(40)))), ((int)(((byte)(40)))), ((int)(((byte)(40)))));
            this.NavigationPanel.Controls.Add(this.NavigationItemsPanel);
            this.NavigationPanel.Location = new System.Drawing.Point(0, 0);
            this.NavigationPanel.Name = "NavigationPanel";
            this.NavigationPanel.Size = new System.Drawing.Size(0, 494);
            this.NavigationPanel.TabIndex = 1;
            // 
            // NavigationItemsPanel
            // 
            this.NavigationItemsPanel.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left)));
            this.NavigationItemsPanel.BackColor = System.Drawing.Color.Transparent;
            this.NavigationItemsPanel.Location = new System.Drawing.Point(0, 53);
            this.NavigationItemsPanel.Name = "NavigationItemsPanel";
            this.NavigationItemsPanel.Size = new System.Drawing.Size(247, 441);
            this.NavigationItemsPanel.TabIndex = 24;
            // 
            // CalculatorContainerPanel
            // 
            this.CalculatorContainerPanel.BackColor = System.Drawing.Color.Transparent;
            this.CalculatorContainerPanel.Dock = System.Windows.Forms.DockStyle.Fill;
            this.CalculatorContainerPanel.Location = new System.Drawing.Point(0, 66);
            this.CalculatorContainerPanel.Name = "CalculatorContainerPanel";
            this.CalculatorContainerPanel.Size = new System.Drawing.Size(328, 428);
            this.CalculatorContainerPanel.TabIndex = 3;
            // 
            // panel2
            // 
            this.panel2.BackColor = System.Drawing.Color.Transparent;
            this.panel2.Controls.Add(this.PageTitleLabel);
            this.panel2.Dock = System.Windows.Forms.DockStyle.Top;
            this.panel2.Location = new System.Drawing.Point(0, 0);
            this.panel2.Name = "panel2";
            this.panel2.Size = new System.Drawing.Size(328, 66);
            this.panel2.TabIndex = 2;
            // 
            // PageTitleLabel
            // 
            this.PageTitleLabel.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.PageTitleLabel.AutoSize = true;
            this.PageTitleLabel.Font = new System.Drawing.Font("Gadugi", 14F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.PageTitleLabel.Location = new System.Drawing.Point(45, 16);
            this.PageTitleLabel.Name = "PageTitleLabel";
            this.PageTitleLabel.Size = new System.Drawing.Size(206, 34);
            this.PageTitleLabel.TabIndex = 0;
            this.PageTitleLabel.Text = "PageTitleLabel";
            // 
            // ShellForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(13F, 28F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(20)))), ((int)(((byte)(20)))), ((int)(((byte)(20)))));
            this.ClientSize = new System.Drawing.Size(328, 494);
            this.Controls.Add(this.panel1);
            this.Font = new System.Drawing.Font("Gadugi", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.ForeColor = System.Drawing.Color.White;
            this.Margin = new System.Windows.Forms.Padding(4);
            this.Name = "ShellForm";
            this.Text = "Calculator";
            this.Load += new System.EventHandler(this.ShellForm_Load);
            this.panel1.ResumeLayout(false);
            this.NavigationPanel.ResumeLayout(false);
            this.panel2.ResumeLayout(false);
            this.panel2.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Panel panel1;
        private System.Windows.Forms.Button NavigationButton;
        private System.Windows.Forms.Panel NavigationPanel;
        private System.Windows.Forms.Panel panel2;
        private System.Windows.Forms.Label PageTitleLabel;
        private System.Windows.Forms.Panel NavigationItemsPanel;
        private System.Windows.Forms.Panel CalculatorContainerPanel;
    }
}

