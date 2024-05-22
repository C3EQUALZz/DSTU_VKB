using WinFormsApp.Core.Classes;

namespace WinFormsApp.Views
{
    public partial class FormMain : Form
    {
        public FormMain()
        {
            InitializeComponent();
        }

        private Color SelectThemeColor()
        {
            var random = new Random();
            var index = random.Next(ColorMapCodes.ColorCodes.Count);
            var colorCode = ColorMapCodes.ColorCodes.Values.ElementAt(index);
            return ColorTranslator.FromHtml(colorCode);
        }

        private void ActivateButton(object sender, EventArgs e)
        {
            if (sender is Button)
            {
                Color color = SelectThemeColor();
                var button = (Button)sender;
                button.BackColor = color;
                button.ForeColor = Color.White;
                button.Font = new Font("JetBrains Mono SemiBold", 9.999999F, FontStyle.Bold);
            }
        }

        private void DisableButton(object sender, EventArgs e)
        {
            foreach (Control control in MenuPanel.Controls)
            {

            }

        }

        private void label1_Click(object sender, EventArgs e)
        {

        }
    }
}
