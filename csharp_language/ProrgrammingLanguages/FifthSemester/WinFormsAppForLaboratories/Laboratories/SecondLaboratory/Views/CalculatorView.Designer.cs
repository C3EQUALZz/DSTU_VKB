namespace WinFormsAppForLaboratories.Laboratories.SecondLaboratory.Views
{
    partial class CalculatorView
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
            Core.Classes.CustomButton buttonBackSpace;
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(CalculatorView));
            Core.Classes.CustomButton buttonPercent;
            Core.Classes.CustomButton buttonClearEntry;
            Core.Classes.CustomButton buttonClear;
            Core.Classes.CustomButton buttonSquareRoot;
            Core.Classes.CustomButton buttonSquare;
            Core.Classes.CustomButton buttonReverseFraction;
            Core.Classes.CustomButton buttonDivision;
            Core.Classes.CustomButton buttonMultiply;
            Core.Classes.CustomButton buttonSubstraction;
            Core.Classes.CustomButton buttonAdd;
            textDisplay1 = new TextBox();
            panelTitle = new Panel();
            iconButton2 = new FontAwesome.Sharp.IconButton();
            iconButton1 = new FontAwesome.Sharp.IconButton();
            buttonExit = new FontAwesome.Sharp.IconButton();
            panelHistory = new Panel();
            buttonClearHistory = new FontAwesome.Sharp.IconButton();
            richTextBoxDisplayHistory = new RichTextBox();
            panel1 = new Panel();
            menuButton = new FontAwesome.Sharp.IconButton();
            buttonHistory = new FontAwesome.Sharp.IconButton();
            textDisplay2 = new TextBox();
            ellipseForm = new Core.Classes.EllipseControl();
            customButton3 = new Core.Classes.CustomButton();
            customButton4 = new Core.Classes.CustomButton();
            customButton5 = new Core.Classes.CustomButton();
            customButton6 = new Core.Classes.CustomButton();
            customButton7 = new Core.Classes.CustomButton();
            buttonNine = new Core.Classes.CustomButton();
            buttonEigth = new Core.Classes.CustomButton();
            buttonSeven = new Core.Classes.CustomButton();
            buttonSix = new Core.Classes.CustomButton();
            buttonFive = new Core.Classes.CustomButton();
            buttonFour = new Core.Classes.CustomButton();
            buttonThree = new Core.Classes.CustomButton();
            buttonTwo = new Core.Classes.CustomButton();
            buttonOne = new Core.Classes.CustomButton();
            buttonDecimal = new Core.Classes.CustomButton();
            buttonZero = new Core.Classes.CustomButton();
            buttonSwapPlusMinus = new Core.Classes.CustomButton();
            buttonEquals = new Core.Classes.CustomButton();
            buttonBackSpace = new Core.Classes.CustomButton();
            buttonPercent = new Core.Classes.CustomButton();
            buttonClearEntry = new Core.Classes.CustomButton();
            buttonClear = new Core.Classes.CustomButton();
            buttonSquareRoot = new Core.Classes.CustomButton();
            buttonSquare = new Core.Classes.CustomButton();
            buttonReverseFraction = new Core.Classes.CustomButton();
            buttonDivision = new Core.Classes.CustomButton();
            buttonMultiply = new Core.Classes.CustomButton();
            buttonSubstraction = new Core.Classes.CustomButton();
            buttonAdd = new Core.Classes.CustomButton();
            panelTitle.SuspendLayout();
            panelHistory.SuspendLayout();
            panel1.SuspendLayout();
            SuspendLayout();
            // 
            // buttonBackSpace
            // 
            buttonBackSpace.BackColor = Color.FromArgb(48, 48, 48);
            buttonBackSpace.BackGroundColor = Color.FromArgb(48, 48, 48);
            buttonBackSpace.BorderRadius = 20;
            buttonBackSpace.BorderSize = 0;
            buttonBackSpace.FlatAppearance.BorderSize = 0;
            buttonBackSpace.FlatStyle = FlatStyle.Flat;
            buttonBackSpace.ForeColor = Color.White;
            buttonBackSpace.Image = (Image)resources.GetObject("buttonBackSpace.Image");
            buttonBackSpace.Location = new Point(272, 217);
            buttonBackSpace.Margin = new Padding(0);
            buttonBackSpace.Name = "buttonBackSpace";
            buttonBackSpace.Size = new Size(80, 53);
            buttonBackSpace.TabIndex = 5;
            buttonBackSpace.TextColor = Color.White;
            buttonBackSpace.UseVisualStyleBackColor = false;
            buttonBackSpace.Click += OnButtonBackSpaceClick;
            // 
            // buttonPercent
            // 
            buttonPercent.BackColor = Color.FromArgb(48, 48, 48);
            buttonPercent.BackGroundColor = Color.FromArgb(48, 48, 48);
            buttonPercent.BorderRadius = 20;
            buttonPercent.BorderSize = 0;
            buttonPercent.FlatAppearance.BorderSize = 0;
            buttonPercent.FlatStyle = FlatStyle.Flat;
            buttonPercent.ForeColor = Color.White;
            buttonPercent.Location = new Point(5, 217);
            buttonPercent.Margin = new Padding(0);
            buttonPercent.Name = "buttonPercent";
            buttonPercent.Size = new Size(80, 53);
            buttonPercent.TabIndex = 12;
            buttonPercent.Text = "%";
            buttonPercent.TextColor = Color.White;
            buttonPercent.UseVisualStyleBackColor = false;
            // 
            // buttonClearEntry
            // 
            buttonClearEntry.BackColor = Color.FromArgb(48, 48, 48);
            buttonClearEntry.BackGroundColor = Color.FromArgb(48, 48, 48);
            buttonClearEntry.BorderRadius = 20;
            buttonClearEntry.BorderSize = 0;
            buttonClearEntry.FlatAppearance.BorderSize = 0;
            buttonClearEntry.FlatStyle = FlatStyle.Flat;
            buttonClearEntry.ForeColor = Color.White;
            buttonClearEntry.Location = new Point(94, 217);
            buttonClearEntry.Margin = new Padding(0);
            buttonClearEntry.Name = "buttonClearEntry";
            buttonClearEntry.Size = new Size(80, 53);
            buttonClearEntry.TabIndex = 13;
            buttonClearEntry.Text = "CE";
            buttonClearEntry.TextColor = Color.White;
            buttonClearEntry.UseVisualStyleBackColor = false;
            // 
            // buttonClear
            // 
            buttonClear.BackColor = Color.FromArgb(48, 48, 48);
            buttonClear.BackGroundColor = Color.FromArgb(48, 48, 48);
            buttonClear.BorderRadius = 20;
            buttonClear.BorderSize = 0;
            buttonClear.FlatAppearance.BorderSize = 0;
            buttonClear.FlatStyle = FlatStyle.Flat;
            buttonClear.ForeColor = Color.White;
            buttonClear.Location = new Point(183, 217);
            buttonClear.Margin = new Padding(0);
            buttonClear.Name = "buttonClear";
            buttonClear.Size = new Size(80, 53);
            buttonClear.TabIndex = 14;
            buttonClear.Text = "C";
            buttonClear.TextColor = Color.White;
            buttonClear.UseVisualStyleBackColor = false;
            // 
            // buttonSquareRoot
            // 
            buttonSquareRoot.BackColor = Color.FromArgb(48, 48, 48);
            buttonSquareRoot.BackGroundColor = Color.FromArgb(48, 48, 48);
            buttonSquareRoot.BorderRadius = 20;
            buttonSquareRoot.BorderSize = 0;
            buttonSquareRoot.FlatAppearance.BorderSize = 0;
            buttonSquareRoot.FlatStyle = FlatStyle.Flat;
            buttonSquareRoot.Font = new Font("Gadugi", 14F);
            buttonSquareRoot.ForeColor = Color.White;
            buttonSquareRoot.Location = new Point(183, 273);
            buttonSquareRoot.Margin = new Padding(0);
            buttonSquareRoot.Name = "buttonSquareRoot";
            buttonSquareRoot.Size = new Size(80, 53);
            buttonSquareRoot.TabIndex = 18;
            buttonSquareRoot.Text = "√𝑥";
            buttonSquareRoot.TextColor = Color.White;
            buttonSquareRoot.UseVisualStyleBackColor = false;
            // 
            // buttonSquare
            // 
            buttonSquare.BackColor = Color.FromArgb(48, 48, 48);
            buttonSquare.BackGroundColor = Color.FromArgb(48, 48, 48);
            buttonSquare.BorderRadius = 20;
            buttonSquare.BorderSize = 0;
            buttonSquare.FlatAppearance.BorderSize = 0;
            buttonSquare.FlatStyle = FlatStyle.Flat;
            buttonSquare.Font = new Font("Gadugi", 14F);
            buttonSquare.ForeColor = Color.White;
            buttonSquare.Location = new Point(94, 273);
            buttonSquare.Margin = new Padding(0);
            buttonSquare.Name = "buttonSquare";
            buttonSquare.Size = new Size(80, 53);
            buttonSquare.TabIndex = 17;
            buttonSquare.Text = "𝑥²";
            buttonSquare.TextColor = Color.White;
            buttonSquare.UseVisualStyleBackColor = false;
            // 
            // buttonReverseFraction
            // 
            buttonReverseFraction.BackColor = Color.FromArgb(48, 48, 48);
            buttonReverseFraction.BackGroundColor = Color.FromArgb(48, 48, 48);
            buttonReverseFraction.BorderRadius = 20;
            buttonReverseFraction.BorderSize = 0;
            buttonReverseFraction.FlatAppearance.BorderSize = 0;
            buttonReverseFraction.FlatStyle = FlatStyle.Flat;
            buttonReverseFraction.Font = new Font("Gadugi", 14F);
            buttonReverseFraction.ForeColor = Color.White;
            buttonReverseFraction.Location = new Point(5, 273);
            buttonReverseFraction.Margin = new Padding(0);
            buttonReverseFraction.Name = "buttonReverseFraction";
            buttonReverseFraction.Size = new Size(80, 53);
            buttonReverseFraction.TabIndex = 16;
            buttonReverseFraction.Text = "⅟𝑥";
            buttonReverseFraction.TextColor = Color.White;
            buttonReverseFraction.UseVisualStyleBackColor = false;
            // 
            // buttonDivision
            // 
            buttonDivision.BackColor = Color.FromArgb(48, 48, 48);
            buttonDivision.BackGroundColor = Color.FromArgb(48, 48, 48);
            buttonDivision.BorderRadius = 20;
            buttonDivision.BorderSize = 0;
            buttonDivision.FlatAppearance.BorderSize = 0;
            buttonDivision.FlatStyle = FlatStyle.Flat;
            buttonDivision.Font = new Font("Gadugi", 14F);
            buttonDivision.ForeColor = Color.White;
            buttonDivision.Location = new Point(272, 273);
            buttonDivision.Margin = new Padding(0);
            buttonDivision.Name = "buttonDivision";
            buttonDivision.Size = new Size(80, 53);
            buttonDivision.TabIndex = 15;
            buttonDivision.Text = "÷";
            buttonDivision.TextColor = Color.White;
            buttonDivision.UseVisualStyleBackColor = false;
            buttonDivision.Click += OnButtonMathOperationClick;
            // 
            // buttonMultiply
            // 
            buttonMultiply.BackColor = Color.FromArgb(48, 48, 48);
            buttonMultiply.BackGroundColor = Color.FromArgb(48, 48, 48);
            buttonMultiply.BorderRadius = 20;
            buttonMultiply.BorderSize = 0;
            buttonMultiply.FlatAppearance.BorderSize = 0;
            buttonMultiply.FlatStyle = FlatStyle.Flat;
            buttonMultiply.Font = new Font("Gadugi", 14F);
            buttonMultiply.ForeColor = Color.White;
            buttonMultiply.Location = new Point(272, 329);
            buttonMultiply.Margin = new Padding(0);
            buttonMultiply.Name = "buttonMultiply";
            buttonMultiply.Size = new Size(80, 53);
            buttonMultiply.TabIndex = 19;
            buttonMultiply.Text = "×";
            buttonMultiply.TextColor = Color.White;
            buttonMultiply.UseVisualStyleBackColor = false;
            buttonMultiply.Click += OnButtonMathOperationClick;
            // 
            // buttonSubstraction
            // 
            buttonSubstraction.BackColor = Color.FromArgb(48, 48, 48);
            buttonSubstraction.BackGroundColor = Color.FromArgb(48, 48, 48);
            buttonSubstraction.BorderRadius = 20;
            buttonSubstraction.BorderSize = 0;
            buttonSubstraction.FlatAppearance.BorderSize = 0;
            buttonSubstraction.FlatStyle = FlatStyle.Flat;
            buttonSubstraction.Font = new Font("Gadugi", 14F);
            buttonSubstraction.ForeColor = Color.White;
            buttonSubstraction.Location = new Point(272, 385);
            buttonSubstraction.Margin = new Padding(0);
            buttonSubstraction.Name = "buttonSubstraction";
            buttonSubstraction.Size = new Size(80, 53);
            buttonSubstraction.TabIndex = 23;
            buttonSubstraction.Text = "-";
            buttonSubstraction.TextColor = Color.White;
            buttonSubstraction.UseVisualStyleBackColor = false;
            buttonSubstraction.Click += OnButtonMathOperationClick;
            // 
            // buttonAdd
            // 
            buttonAdd.BackColor = Color.FromArgb(48, 48, 48);
            buttonAdd.BackGroundColor = Color.FromArgb(48, 48, 48);
            buttonAdd.BorderRadius = 20;
            buttonAdd.BorderSize = 0;
            buttonAdd.FlatAppearance.BorderSize = 0;
            buttonAdd.FlatStyle = FlatStyle.Flat;
            buttonAdd.Font = new Font("Gadugi", 14F);
            buttonAdd.ForeColor = Color.White;
            buttonAdd.Location = new Point(272, 441);
            buttonAdd.Margin = new Padding(0);
            buttonAdd.Name = "buttonAdd";
            buttonAdd.Size = new Size(80, 53);
            buttonAdd.TabIndex = 27;
            buttonAdd.Text = "+";
            buttonAdd.TextColor = Color.White;
            buttonAdd.UseVisualStyleBackColor = false;
            buttonAdd.Click += OnButtonMathOperationClick;
            // 
            // textDisplay1
            // 
            textDisplay1.BackColor = Color.FromArgb(32, 32, 32);
            textDisplay1.BorderStyle = BorderStyle.None;
            textDisplay1.Dock = DockStyle.Top;
            textDisplay1.Font = new Font("Gadugi", 30F, FontStyle.Bold);
            textDisplay1.ForeColor = Color.WhiteSmoke;
            textDisplay1.Location = new Point(0, 105);
            textDisplay1.Margin = new Padding(0);
            textDisplay1.Multiline = true;
            textDisplay1.Name = "textDisplay1";
            textDisplay1.Size = new Size(360, 60);
            textDisplay1.TabIndex = 4;
            textDisplay1.Text = "0";
            textDisplay1.TextAlign = HorizontalAlignment.Right;
            // 
            // panelTitle
            // 
            panelTitle.Controls.Add(iconButton2);
            panelTitle.Controls.Add(iconButton1);
            panelTitle.Controls.Add(buttonExit);
            panelTitle.Dock = DockStyle.Top;
            panelTitle.Location = new Point(0, 0);
            panelTitle.Margin = new Padding(0);
            panelTitle.Name = "panelTitle";
            panelTitle.Size = new Size(360, 40);
            panelTitle.TabIndex = 0;
            // 
            // iconButton2
            // 
            iconButton2.Dock = DockStyle.Right;
            iconButton2.FlatAppearance.BorderSize = 0;
            iconButton2.FlatStyle = FlatStyle.Flat;
            iconButton2.Font = new Font("Gadugi", 12F, FontStyle.Regular, GraphicsUnit.Point, 0);
            iconButton2.ForeColor = Color.Transparent;
            iconButton2.IconChar = FontAwesome.Sharp.IconChar.Minus;
            iconButton2.IconColor = Color.White;
            iconButton2.IconFont = FontAwesome.Sharp.IconFont.Auto;
            iconButton2.IconSize = 17;
            iconButton2.Location = new Point(210, 0);
            iconButton2.Margin = new Padding(0);
            iconButton2.Name = "iconButton2";
            iconButton2.Size = new Size(50, 40);
            iconButton2.TabIndex = 4;
            iconButton2.UseVisualStyleBackColor = true;
            // 
            // iconButton1
            // 
            iconButton1.Dock = DockStyle.Right;
            iconButton1.FlatAppearance.BorderSize = 0;
            iconButton1.FlatStyle = FlatStyle.Flat;
            iconButton1.ForeColor = Color.Transparent;
            iconButton1.IconChar = FontAwesome.Sharp.IconChar.SquareFull;
            iconButton1.IconColor = Color.White;
            iconButton1.IconFont = FontAwesome.Sharp.IconFont.Auto;
            iconButton1.IconSize = 15;
            iconButton1.Location = new Point(260, 0);
            iconButton1.Margin = new Padding(0);
            iconButton1.Name = "iconButton1";
            iconButton1.Size = new Size(50, 40);
            iconButton1.TabIndex = 3;
            iconButton1.UseVisualStyleBackColor = true;
            // 
            // buttonExit
            // 
            buttonExit.Dock = DockStyle.Right;
            buttonExit.FlatAppearance.BorderSize = 0;
            buttonExit.FlatAppearance.MouseOverBackColor = Color.Red;
            buttonExit.FlatStyle = FlatStyle.Flat;
            buttonExit.ForeColor = Color.Transparent;
            buttonExit.IconChar = FontAwesome.Sharp.IconChar.Multiply;
            buttonExit.IconColor = Color.White;
            buttonExit.IconFont = FontAwesome.Sharp.IconFont.Auto;
            buttonExit.IconSize = 16;
            buttonExit.Location = new Point(310, 0);
            buttonExit.Margin = new Padding(0);
            buttonExit.Name = "buttonExit";
            buttonExit.Size = new Size(50, 40);
            buttonExit.TabIndex = 2;
            buttonExit.UseVisualStyleBackColor = true;
            // 
            // panelHistory
            // 
            panelHistory.Controls.Add(buttonClearHistory);
            panelHistory.Controls.Add(richTextBoxDisplayHistory);
            panelHistory.Dock = DockStyle.Bottom;
            panelHistory.Location = new Point(0, 565);
            panelHistory.Margin = new Padding(10, 0, 10, 0);
            panelHistory.Name = "panelHistory";
            panelHistory.Size = new Size(360, 5);
            panelHistory.TabIndex = 1;
            // 
            // buttonClearHistory
            // 
            buttonClearHistory.Dock = DockStyle.Bottom;
            buttonClearHistory.FlatAppearance.BorderSize = 0;
            buttonClearHistory.FlatStyle = FlatStyle.Flat;
            buttonClearHistory.Font = new Font("Gadugi", 12F, FontStyle.Regular, GraphicsUnit.Point, 0);
            buttonClearHistory.ForeColor = Color.Transparent;
            buttonClearHistory.IconChar = FontAwesome.Sharp.IconChar.Trash;
            buttonClearHistory.IconColor = Color.White;
            buttonClearHistory.IconFont = FontAwesome.Sharp.IconFont.Auto;
            buttonClearHistory.IconSize = 25;
            buttonClearHistory.Location = new Point(0, -35);
            buttonClearHistory.Margin = new Padding(0);
            buttonClearHistory.Name = "buttonClearHistory";
            buttonClearHistory.Size = new Size(360, 40);
            buttonClearHistory.TabIndex = 5;
            buttonClearHistory.UseVisualStyleBackColor = true;
            buttonClearHistory.Click += OnButtonClearHistoryClick;
            // 
            // richTextBoxDisplayHistory
            // 
            richTextBoxDisplayHistory.BackColor = Color.FromArgb(32, 32, 32);
            richTextBoxDisplayHistory.BorderStyle = BorderStyle.None;
            richTextBoxDisplayHistory.Dock = DockStyle.Fill;
            richTextBoxDisplayHistory.ForeColor = Color.Silver;
            richTextBoxDisplayHistory.Location = new Point(0, 0);
            richTextBoxDisplayHistory.Margin = new Padding(0);
            richTextBoxDisplayHistory.Name = "richTextBoxDisplayHistory";
            richTextBoxDisplayHistory.ScrollBars = RichTextBoxScrollBars.Horizontal;
            richTextBoxDisplayHistory.Size = new Size(360, 5);
            richTextBoxDisplayHistory.TabIndex = 6;
            richTextBoxDisplayHistory.Text = "";
            // 
            // panel1
            // 
            panel1.Controls.Add(menuButton);
            panel1.Controls.Add(buttonHistory);
            panel1.Dock = DockStyle.Top;
            panel1.Location = new Point(0, 40);
            panel1.Margin = new Padding(0);
            panel1.Name = "panel1";
            panel1.Size = new Size(360, 40);
            panel1.TabIndex = 2;
            // 
            // menuButton
            // 
            menuButton.Dock = DockStyle.Left;
            menuButton.FlatAppearance.BorderSize = 0;
            menuButton.FlatAppearance.MouseOverBackColor = Color.Red;
            menuButton.FlatStyle = FlatStyle.Flat;
            menuButton.Font = new Font("Gadugi", 12F, FontStyle.Regular, GraphicsUnit.Point, 0);
            menuButton.ForeColor = Color.Transparent;
            menuButton.IconChar = FontAwesome.Sharp.IconChar.AlignJustify;
            menuButton.IconColor = Color.White;
            menuButton.IconFont = FontAwesome.Sharp.IconFont.Auto;
            menuButton.IconSize = 25;
            menuButton.Location = new Point(0, 0);
            menuButton.Margin = new Padding(0);
            menuButton.Name = "menuButton";
            menuButton.Size = new Size(50, 40);
            menuButton.TabIndex = 4;
            menuButton.UseVisualStyleBackColor = true;
            // 
            // buttonHistory
            // 
            buttonHistory.Dock = DockStyle.Right;
            buttonHistory.FlatAppearance.BorderSize = 0;
            buttonHistory.FlatAppearance.MouseOverBackColor = Color.Red;
            buttonHistory.FlatStyle = FlatStyle.Flat;
            buttonHistory.ForeColor = Color.Transparent;
            buttonHistory.IconChar = FontAwesome.Sharp.IconChar.ClockRotateLeft;
            buttonHistory.IconColor = Color.White;
            buttonHistory.IconFont = FontAwesome.Sharp.IconFont.Auto;
            buttonHistory.IconSize = 25;
            buttonHistory.Location = new Point(310, 0);
            buttonHistory.Margin = new Padding(0);
            buttonHistory.Name = "buttonHistory";
            buttonHistory.Size = new Size(50, 40);
            buttonHistory.TabIndex = 2;
            buttonHistory.UseVisualStyleBackColor = true;
            buttonHistory.Click += OnButtonHistoryClick;
            // 
            // textDisplay2
            // 
            textDisplay2.BackColor = Color.FromArgb(32, 32, 32);
            textDisplay2.BorderStyle = BorderStyle.None;
            textDisplay2.Dock = DockStyle.Top;
            textDisplay2.Font = new Font("Gadugi", 13.8F, FontStyle.Regular, GraphicsUnit.Point, 0);
            textDisplay2.ForeColor = Color.Silver;
            textDisplay2.Location = new Point(0, 80);
            textDisplay2.Margin = new Padding(0);
            textDisplay2.Multiline = true;
            textDisplay2.Name = "textDisplay2";
            textDisplay2.Size = new Size(360, 25);
            textDisplay2.TabIndex = 3;
            textDisplay2.TextAlign = HorizontalAlignment.Right;
            // 
            // ellipseForm
            // 
            ellipseForm.CornerRadius = 20;
            ellipseForm.TargetControl = this;
            // 
            // customButton3
            // 
            customButton3.BackColor = Color.FromArgb(32, 32, 32);
            customButton3.BackGroundColor = Color.FromArgb(32, 32, 32);
            customButton3.BorderRadius = 20;
            customButton3.BorderSize = 0;
            customButton3.FlatAppearance.BorderSize = 0;
            customButton3.FlatStyle = FlatStyle.Flat;
            customButton3.ForeColor = Color.White;
            customButton3.Location = new Point(295, 178);
            customButton3.Margin = new Padding(0);
            customButton3.Name = "customButton3";
            customButton3.Size = new Size(55, 30);
            customButton3.TabIndex = 7;
            customButton3.Text = "MS";
            customButton3.TextColor = Color.White;
            customButton3.UseVisualStyleBackColor = false;
            // 
            // customButton4
            // 
            customButton4.BackColor = Color.FromArgb(32, 32, 32);
            customButton4.BackGroundColor = Color.FromArgb(32, 32, 32);
            customButton4.BorderRadius = 20;
            customButton4.BorderSize = 0;
            customButton4.FlatAppearance.BorderSize = 0;
            customButton4.FlatStyle = FlatStyle.Flat;
            customButton4.ForeColor = Color.White;
            customButton4.Location = new Point(223, 178);
            customButton4.Margin = new Padding(0);
            customButton4.Name = "customButton4";
            customButton4.Size = new Size(55, 30);
            customButton4.TabIndex = 8;
            customButton4.Text = "M-";
            customButton4.TextColor = Color.White;
            customButton4.UseVisualStyleBackColor = false;
            // 
            // customButton5
            // 
            customButton5.BackColor = Color.FromArgb(32, 32, 32);
            customButton5.BackGroundColor = Color.FromArgb(32, 32, 32);
            customButton5.BorderRadius = 20;
            customButton5.BorderSize = 0;
            customButton5.FlatAppearance.BorderSize = 0;
            customButton5.FlatStyle = FlatStyle.Flat;
            customButton5.ForeColor = Color.White;
            customButton5.Location = new Point(151, 178);
            customButton5.Margin = new Padding(0);
            customButton5.Name = "customButton5";
            customButton5.Size = new Size(55, 30);
            customButton5.TabIndex = 9;
            customButton5.Text = "M+";
            customButton5.TextColor = Color.White;
            customButton5.UseVisualStyleBackColor = false;
            // 
            // customButton6
            // 
            customButton6.BackColor = Color.FromArgb(32, 32, 32);
            customButton6.BackGroundColor = Color.FromArgb(32, 32, 32);
            customButton6.BorderRadius = 20;
            customButton6.BorderSize = 0;
            customButton6.FlatAppearance.BorderSize = 0;
            customButton6.FlatStyle = FlatStyle.Flat;
            customButton6.ForeColor = Color.White;
            customButton6.Location = new Point(79, 178);
            customButton6.Margin = new Padding(0);
            customButton6.Name = "customButton6";
            customButton6.Size = new Size(55, 30);
            customButton6.TabIndex = 10;
            customButton6.Text = "MR";
            customButton6.TextColor = Color.White;
            customButton6.UseVisualStyleBackColor = false;
            // 
            // customButton7
            // 
            customButton7.BackColor = Color.FromArgb(32, 32, 32);
            customButton7.BackGroundColor = Color.FromArgb(32, 32, 32);
            customButton7.BorderRadius = 20;
            customButton7.BorderSize = 0;
            customButton7.FlatAppearance.BorderSize = 0;
            customButton7.FlatStyle = FlatStyle.Flat;
            customButton7.ForeColor = Color.White;
            customButton7.Location = new Point(7, 178);
            customButton7.Margin = new Padding(0);
            customButton7.Name = "customButton7";
            customButton7.Size = new Size(55, 30);
            customButton7.TabIndex = 11;
            customButton7.Text = "MC";
            customButton7.TextColor = Color.White;
            customButton7.UseVisualStyleBackColor = false;
            // 
            // buttonNine
            // 
            buttonNine.BackColor = Color.FromArgb(60, 60, 60);
            buttonNine.BackGroundColor = Color.FromArgb(60, 60, 60);
            buttonNine.BorderRadius = 20;
            buttonNine.BorderSize = 0;
            buttonNine.FlatAppearance.BorderSize = 0;
            buttonNine.FlatStyle = FlatStyle.Flat;
            buttonNine.Font = new Font("Gadugi", 12F);
            buttonNine.ForeColor = Color.White;
            buttonNine.Location = new Point(183, 329);
            buttonNine.Margin = new Padding(0);
            buttonNine.Name = "buttonNine";
            buttonNine.Size = new Size(80, 53);
            buttonNine.TabIndex = 22;
            buttonNine.Text = "9";
            buttonNine.TextColor = Color.White;
            buttonNine.UseVisualStyleBackColor = false;
            buttonNine.Click += OnButtonNumberClick;
            // 
            // buttonEigth
            // 
            buttonEigth.BackColor = Color.FromArgb(60, 60, 60);
            buttonEigth.BackGroundColor = Color.FromArgb(60, 60, 60);
            buttonEigth.BorderRadius = 20;
            buttonEigth.BorderSize = 0;
            buttonEigth.FlatAppearance.BorderSize = 0;
            buttonEigth.FlatStyle = FlatStyle.Flat;
            buttonEigth.Font = new Font("Gadugi", 12F);
            buttonEigth.ForeColor = Color.White;
            buttonEigth.Location = new Point(94, 329);
            buttonEigth.Margin = new Padding(0);
            buttonEigth.Name = "buttonEigth";
            buttonEigth.Size = new Size(80, 53);
            buttonEigth.TabIndex = 21;
            buttonEigth.Text = "8";
            buttonEigth.TextColor = Color.White;
            buttonEigth.UseVisualStyleBackColor = false;
            buttonEigth.Click += OnButtonNumberClick;
            // 
            // buttonSeven
            // 
            buttonSeven.BackColor = Color.FromArgb(60, 60, 60);
            buttonSeven.BackGroundColor = Color.FromArgb(60, 60, 60);
            buttonSeven.BorderRadius = 20;
            buttonSeven.BorderSize = 0;
            buttonSeven.FlatAppearance.BorderSize = 0;
            buttonSeven.FlatStyle = FlatStyle.Flat;
            buttonSeven.Font = new Font("Gadugi", 12F);
            buttonSeven.ForeColor = Color.White;
            buttonSeven.Location = new Point(5, 329);
            buttonSeven.Margin = new Padding(0);
            buttonSeven.Name = "buttonSeven";
            buttonSeven.Size = new Size(80, 53);
            buttonSeven.TabIndex = 20;
            buttonSeven.Text = "7";
            buttonSeven.TextColor = Color.White;
            buttonSeven.UseVisualStyleBackColor = false;
            buttonSeven.Click += OnButtonNumberClick;
            // 
            // buttonSix
            // 
            buttonSix.BackColor = Color.FromArgb(60, 60, 60);
            buttonSix.BackGroundColor = Color.FromArgb(60, 60, 60);
            buttonSix.BorderRadius = 20;
            buttonSix.BorderSize = 0;
            buttonSix.FlatAppearance.BorderSize = 0;
            buttonSix.FlatStyle = FlatStyle.Flat;
            buttonSix.Font = new Font("Gadugi", 12F);
            buttonSix.ForeColor = Color.White;
            buttonSix.Location = new Point(183, 385);
            buttonSix.Margin = new Padding(0);
            buttonSix.Name = "buttonSix";
            buttonSix.Size = new Size(80, 53);
            buttonSix.TabIndex = 26;
            buttonSix.Text = "6";
            buttonSix.TextColor = Color.White;
            buttonSix.UseVisualStyleBackColor = false;
            buttonSix.Click += OnButtonNumberClick;
            // 
            // buttonFive
            // 
            buttonFive.BackColor = Color.FromArgb(60, 60, 60);
            buttonFive.BackGroundColor = Color.FromArgb(60, 60, 60);
            buttonFive.BorderRadius = 20;
            buttonFive.BorderSize = 0;
            buttonFive.FlatAppearance.BorderSize = 0;
            buttonFive.FlatStyle = FlatStyle.Flat;
            buttonFive.Font = new Font("Gadugi", 12F);
            buttonFive.ForeColor = Color.White;
            buttonFive.Location = new Point(94, 385);
            buttonFive.Margin = new Padding(0);
            buttonFive.Name = "buttonFive";
            buttonFive.Size = new Size(80, 53);
            buttonFive.TabIndex = 25;
            buttonFive.Text = "5";
            buttonFive.TextColor = Color.White;
            buttonFive.UseVisualStyleBackColor = false;
            buttonFive.Click += OnButtonNumberClick;
            // 
            // buttonFour
            // 
            buttonFour.BackColor = Color.FromArgb(60, 60, 60);
            buttonFour.BackGroundColor = Color.FromArgb(60, 60, 60);
            buttonFour.BorderRadius = 20;
            buttonFour.BorderSize = 0;
            buttonFour.FlatAppearance.BorderSize = 0;
            buttonFour.FlatStyle = FlatStyle.Flat;
            buttonFour.Font = new Font("Gadugi", 12F);
            buttonFour.ForeColor = Color.White;
            buttonFour.Location = new Point(5, 385);
            buttonFour.Margin = new Padding(0);
            buttonFour.Name = "buttonFour";
            buttonFour.Size = new Size(80, 53);
            buttonFour.TabIndex = 24;
            buttonFour.Text = "4";
            buttonFour.TextColor = Color.White;
            buttonFour.UseVisualStyleBackColor = false;
            buttonFour.Click += OnButtonNumberClick;
            // 
            // buttonThree
            // 
            buttonThree.BackColor = Color.FromArgb(60, 60, 60);
            buttonThree.BackGroundColor = Color.FromArgb(60, 60, 60);
            buttonThree.BorderRadius = 20;
            buttonThree.BorderSize = 0;
            buttonThree.FlatAppearance.BorderSize = 0;
            buttonThree.FlatStyle = FlatStyle.Flat;
            buttonThree.Font = new Font("Gadugi", 12F);
            buttonThree.ForeColor = Color.White;
            buttonThree.Location = new Point(183, 441);
            buttonThree.Margin = new Padding(0);
            buttonThree.Name = "buttonThree";
            buttonThree.Size = new Size(80, 53);
            buttonThree.TabIndex = 30;
            buttonThree.Text = "3";
            buttonThree.TextColor = Color.White;
            buttonThree.UseVisualStyleBackColor = false;
            buttonThree.Click += OnButtonNumberClick;
            // 
            // buttonTwo
            // 
            buttonTwo.BackColor = Color.FromArgb(60, 60, 60);
            buttonTwo.BackGroundColor = Color.FromArgb(60, 60, 60);
            buttonTwo.BorderRadius = 20;
            buttonTwo.BorderSize = 0;
            buttonTwo.FlatAppearance.BorderSize = 0;
            buttonTwo.FlatStyle = FlatStyle.Flat;
            buttonTwo.Font = new Font("Gadugi", 12F);
            buttonTwo.ForeColor = Color.White;
            buttonTwo.Location = new Point(94, 441);
            buttonTwo.Margin = new Padding(0);
            buttonTwo.Name = "buttonTwo";
            buttonTwo.Size = new Size(80, 53);
            buttonTwo.TabIndex = 29;
            buttonTwo.Text = "2";
            buttonTwo.TextColor = Color.White;
            buttonTwo.UseVisualStyleBackColor = false;
            buttonTwo.Click += OnButtonNumberClick;
            // 
            // buttonOne
            // 
            buttonOne.BackColor = Color.FromArgb(60, 60, 60);
            buttonOne.BackGroundColor = Color.FromArgb(60, 60, 60);
            buttonOne.BorderRadius = 20;
            buttonOne.BorderSize = 0;
            buttonOne.FlatAppearance.BorderSize = 0;
            buttonOne.FlatStyle = FlatStyle.Flat;
            buttonOne.Font = new Font("Gadugi", 12F);
            buttonOne.ForeColor = Color.White;
            buttonOne.Location = new Point(5, 441);
            buttonOne.Margin = new Padding(0);
            buttonOne.Name = "buttonOne";
            buttonOne.Size = new Size(80, 53);
            buttonOne.TabIndex = 28;
            buttonOne.Text = "1";
            buttonOne.TextColor = Color.White;
            buttonOne.UseVisualStyleBackColor = false;
            buttonOne.Click += OnButtonNumberClick;
            // 
            // buttonDecimal
            // 
            buttonDecimal.BackColor = Color.FromArgb(60, 60, 60);
            buttonDecimal.BackGroundColor = Color.FromArgb(60, 60, 60);
            buttonDecimal.BorderRadius = 20;
            buttonDecimal.BorderSize = 0;
            buttonDecimal.FlatAppearance.BorderSize = 0;
            buttonDecimal.FlatStyle = FlatStyle.Flat;
            buttonDecimal.Font = new Font("Gadugi", 14F);
            buttonDecimal.ForeColor = Color.White;
            buttonDecimal.Location = new Point(183, 497);
            buttonDecimal.Margin = new Padding(0);
            buttonDecimal.Name = "buttonDecimal";
            buttonDecimal.Size = new Size(80, 53);
            buttonDecimal.TabIndex = 34;
            buttonDecimal.Text = ".";
            buttonDecimal.TextColor = Color.White;
            buttonDecimal.UseVisualStyleBackColor = false;
            buttonDecimal.Click += OnButtonNumberClick;
            // 
            // buttonZero
            // 
            buttonZero.BackColor = Color.FromArgb(60, 60, 60);
            buttonZero.BackGroundColor = Color.FromArgb(60, 60, 60);
            buttonZero.BorderRadius = 20;
            buttonZero.BorderSize = 0;
            buttonZero.FlatAppearance.BorderSize = 0;
            buttonZero.FlatStyle = FlatStyle.Flat;
            buttonZero.Font = new Font("Gadugi", 12F);
            buttonZero.ForeColor = Color.White;
            buttonZero.Location = new Point(94, 497);
            buttonZero.Margin = new Padding(0);
            buttonZero.Name = "buttonZero";
            buttonZero.Size = new Size(80, 53);
            buttonZero.TabIndex = 33;
            buttonZero.Text = "0";
            buttonZero.TextColor = Color.White;
            buttonZero.UseVisualStyleBackColor = false;
            buttonZero.Click += OnButtonNumberClick;
            // 
            // buttonSwapPlusMinus
            // 
            buttonSwapPlusMinus.BackColor = Color.FromArgb(60, 60, 60);
            buttonSwapPlusMinus.BackGroundColor = Color.FromArgb(60, 60, 60);
            buttonSwapPlusMinus.BorderRadius = 20;
            buttonSwapPlusMinus.BorderSize = 0;
            buttonSwapPlusMinus.FlatAppearance.BorderSize = 0;
            buttonSwapPlusMinus.FlatStyle = FlatStyle.Flat;
            buttonSwapPlusMinus.Font = new Font("Gadugi", 14F);
            buttonSwapPlusMinus.ForeColor = Color.White;
            buttonSwapPlusMinus.Location = new Point(5, 497);
            buttonSwapPlusMinus.Margin = new Padding(0);
            buttonSwapPlusMinus.Name = "buttonSwapPlusMinus";
            buttonSwapPlusMinus.Size = new Size(80, 53);
            buttonSwapPlusMinus.TabIndex = 32;
            buttonSwapPlusMinus.Text = "±";
            buttonSwapPlusMinus.TextColor = Color.White;
            buttonSwapPlusMinus.UseVisualStyleBackColor = false;
            // 
            // buttonEquals
            // 
            buttonEquals.BackColor = Color.FromArgb(240, 129, 105);
            buttonEquals.BackGroundColor = Color.FromArgb(240, 129, 105);
            buttonEquals.BorderRadius = 20;
            buttonEquals.BorderSize = 0;
            buttonEquals.FlatAppearance.BorderSize = 0;
            buttonEquals.FlatStyle = FlatStyle.Flat;
            buttonEquals.Font = new Font("Gadugi", 14F);
            buttonEquals.ForeColor = Color.Black;
            buttonEquals.Location = new Point(272, 497);
            buttonEquals.Margin = new Padding(0);
            buttonEquals.Name = "buttonEquals";
            buttonEquals.Size = new Size(80, 53);
            buttonEquals.TabIndex = 31;
            buttonEquals.Text = "=";
            buttonEquals.TextColor = Color.Black;
            buttonEquals.UseVisualStyleBackColor = false;
            buttonEquals.Click += OnButtonEqualsClick;
            // 
            // CalculatorView
            // 
            AutoScaleMode = AutoScaleMode.None;
            BackColor = Color.FromArgb(32, 32, 32);
            ClientSize = new Size(360, 570);
            Controls.Add(panelHistory);
            Controls.Add(buttonDecimal);
            Controls.Add(buttonZero);
            Controls.Add(buttonSwapPlusMinus);
            Controls.Add(buttonEquals);
            Controls.Add(buttonThree);
            Controls.Add(buttonTwo);
            Controls.Add(buttonOne);
            Controls.Add(buttonAdd);
            Controls.Add(buttonSix);
            Controls.Add(buttonFive);
            Controls.Add(buttonFour);
            Controls.Add(buttonSubstraction);
            Controls.Add(buttonNine);
            Controls.Add(buttonEigth);
            Controls.Add(buttonSeven);
            Controls.Add(buttonMultiply);
            Controls.Add(buttonSquareRoot);
            Controls.Add(buttonSquare);
            Controls.Add(buttonReverseFraction);
            Controls.Add(buttonDivision);
            Controls.Add(buttonClear);
            Controls.Add(buttonClearEntry);
            Controls.Add(buttonPercent);
            Controls.Add(customButton7);
            Controls.Add(customButton6);
            Controls.Add(customButton5);
            Controls.Add(customButton4);
            Controls.Add(customButton3);
            Controls.Add(buttonBackSpace);
            Controls.Add(textDisplay1);
            Controls.Add(textDisplay2);
            Controls.Add(panel1);
            Controls.Add(panelTitle);
            Font = new Font("Gadugi", 12F, FontStyle.Regular, GraphicsUnit.Point, 0);
            ForeColor = Color.White;
            FormBorderStyle = FormBorderStyle.None;
            Icon = (Icon)resources.GetObject("$this.Icon");
            Name = "CalculatorView";
            StartPosition = FormStartPosition.CenterScreen;
            Text = "Калькулятор";
            panelTitle.ResumeLayout(false);
            panelHistory.ResumeLayout(false);
            panel1.ResumeLayout(false);
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Panel panelTitle;
        private Panel panelHistory;
        private Button button1;
        private FontAwesome.Sharp.IconButton buttonExit;
        private FontAwesome.Sharp.IconButton iconButton2;
        private FontAwesome.Sharp.IconButton iconButton1;
        private Panel panel1;
        private FontAwesome.Sharp.IconButton menuButton;
        private FontAwesome.Sharp.IconButton buttonHistory;
        private TextBox textDisplay2;
        private TextBox textDisplay1;
        private FontAwesome.Sharp.IconButton buttonClearHistory;
        private RichTextBox richTextBoxDisplayHistory;
        private Core.Classes.EllipseControl ellipseForm;
        private Core.Classes.CustomButton buttonBackSpace;
        private Core.Classes.CustomButton customButton7;
        private Core.Classes.CustomButton customButton6;
        private Core.Classes.CustomButton customButton5;
        private Core.Classes.CustomButton customButton4;
        private Core.Classes.CustomButton customButton3;
        private Core.Classes.CustomButton buttonPercent;
        private Core.Classes.CustomButton buttonClear;
        private Core.Classes.CustomButton buttonClearEntry;
        private Core.Classes.CustomButton buttonSquareRoot;
        private Core.Classes.CustomButton buttonSquare;
        private Core.Classes.CustomButton buttonReverseFraction;
        private Core.Classes.CustomButton buttonDivision;
        private Core.Classes.CustomButton buttonNine;
        private Core.Classes.CustomButton buttonEigth;
        private Core.Classes.CustomButton buttonSeven;
        private Core.Classes.CustomButton buttonMultiply;
        private Core.Classes.CustomButton buttonSix;
        private Core.Classes.CustomButton buttonFive;
        private Core.Classes.CustomButton buttonFour;
        private Core.Classes.CustomButton buttonSubstraction;
        private Core.Classes.CustomButton buttonThree;
        private Core.Classes.CustomButton buttonTwo;
        private Core.Classes.CustomButton buttonOne;
        private Core.Classes.CustomButton buttonAdd;
        private Core.Classes.CustomButton buttonDecimal;
        private Core.Classes.CustomButton buttonZero;
        private Core.Classes.CustomButton buttonSwapPlusMinus;
        private Core.Classes.CustomButton buttonEquals;
    }
}