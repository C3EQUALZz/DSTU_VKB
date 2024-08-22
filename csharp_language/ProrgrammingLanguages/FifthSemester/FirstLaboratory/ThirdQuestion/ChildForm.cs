namespace FirstLaboratory.ThirdQuestion
{
    public partial class ChildForm : Form
    {
        public ChildForm()
        {
            InitializeComponent();
        }

        private void ToggleMenuItem_Click(object sender, EventArgs e)
        {
            if (ToggleMenuItem.Checked)
            {
                ToggleMenuItem.Checked = false;
                ChildTextBox.ForeColor = Color.Black;
            }
            else
            {
                ToggleMenuItem.Checked = true;
                ChildTextBox.ForeColor = Color.Blue;
            }
        }
    }
}
