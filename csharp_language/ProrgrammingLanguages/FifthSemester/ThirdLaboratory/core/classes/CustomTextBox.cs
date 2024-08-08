using System;
using System.Drawing;
using System.Windows.Forms;

namespace ThirdLaboratory.forms
{
    public partial class CustomTextBox : UserControl
    {
        private bool isFocused = false;
        private string txt = "label";
        private bool pass = false;
        private bool multi = false;
        private Color backColor = Color.White;
        private Color foreColor = Color.Black;
        private string TextBox;
        private int borderRadius = 20;
        private int borderWidth = 2;
        private Color borderColor = Color.Black;

        public CustomTextBox()
        {
            InitializeComponent();
            this.Paint += CustomTextBox_Paint;
        }

        public new string Text
        {
            get => txt;
            set { txt = value; Invalidate(); }
        }

        public bool MultiLine
        {
            get => multi;
            set { multi = value; Invalidate(); }
        }

        public bool Password
        {
            get => pass;
            set { pass = value; Invalidate(); }
        }

        public Color BackgroundColor
        {
            get => backColor;
            set { backColor = value; Invalidate(); }
        }

        public new Color ForeColor
        {
            get => foreColor;
            set { foreColor = value; Invalidate(); }
        }

        public int BorderRadius
        {
            get => borderRadius;
            set { borderRadius = value; Invalidate(); }
        }

        public int BorderWidth
        {
            get => borderWidth;
            set { borderWidth = value; Invalidate(); }
        }

        public Color BorderColor
        {
            get => borderColor;
            set { borderColor = value; Invalidate(); }
        }

        private void LabelTimer_Tick(object sender, EventArgs e)
        {
            int y = label1.Location.Y;

            if (!isFocused)
            {
                y -= 2;
                if (y <= 11)
                {
                    isFocused = true;
                    labelTimer.Stop();
                    label1.Font = new Font("Segoe UI", 8);
                    y = 11;
                    label1.ForeColor = Color.Silver;
                }
            }
            else
            {
                y += 2;
                if (y >= 27)
                {
                    isFocused = false;
                    labelTimer.Stop();
                    label1.Font = new Font("Segoe UI", 10);
                    y = 27;
                    label1.ForeColor = Color.Black;
                }
            }

            label1.Location = new Point(label1.Location.X, y);
        }

        private void TextBox1_Enter(object sender, EventArgs e)
        {
            if (textBox1.Text == "")
                labelTimer.Start();
        }

        private void TextBox1_Leave(object sender, EventArgs e)
        {
            if (textBox1.Text == "")
                labelTimer.Start();
        }

        private void CustomTextBox_Paint(object sender, PaintEventArgs e)
        {
            // Заливка фона
            e.Graphics.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.AntiAlias;
            using (var path = new System.Drawing.Drawing2D.GraphicsPath())
            {
                var rect = new Rectangle(0, 0, Width - 1, Height - 1);
                path.AddArc(rect.Left, rect.Top, borderRadius, borderRadius, 180, 90);
                path.AddArc(rect.Right - borderRadius, rect.Top, borderRadius, borderRadius, 270, 90);
                path.AddArc(rect.Right - borderRadius, rect.Bottom - borderRadius, borderRadius, borderRadius, 0, 90);
                path.AddArc(rect.Left, rect.Bottom - borderRadius, borderRadius, borderRadius, 90, 90);
                path.CloseFigure();

                // Фон
                using (var brush = new SolidBrush(BackgroundColor))
                {
                    e.Graphics.FillPath(brush, path);
                }

                // Обводка
                using (var pen = new Pen(BorderColor, BorderWidth))
                {
                    e.Graphics.DrawPath(pen, path);
                }
            }

            // Настройки для текстового поля
            textBox1.BackColor = BackgroundColor;
            textBox1.ForeColor = ForeColor;
            textBox1.BorderStyle = BorderStyle.None;
            textBox1.Multiline = MultiLine;
            textBox1.UseSystemPasswordChar = Password;

            label1.Text = Text;
            label1.BackColor = BackgroundColor;
            label1.ForeColor = ForeColor;

            textBox1.Location = new Point(borderWidth, label1.Bottom);
            textBox1.Width = Width - 2 * borderWidth;
            textBox1.Height = Height - label1.Bottom - borderWidth;
        }

        private void CustomTextBox_Load(object sender, EventArgs e)
        {
            textBox1.UseSystemPasswordChar = Password;
        }

        private void TextBox1_TextChanged(object sender, EventArgs e)
        {
            TextBox = textBox1.Text;
        }
    }
}
