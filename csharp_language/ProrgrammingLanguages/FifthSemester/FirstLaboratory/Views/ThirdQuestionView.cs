using FirstLaboratory.Core.Interfaces.ThirdQuestion;

namespace FirstLaboratory.ThirdQuestion
{
    public partial class ThirdQuestionView : Form
    {
        private int openDocuments = 0;
        private readonly IThirdQuestionPresenter _presenter;

        public ThirdQuestionView()
        {
            InitializeComponent();
            
        }

        private void ExitMenuItem_Click(object sender, EventArgs e)
        {
            Close();
        }

        private void WindowCascadeMenuItem_Click(object sender, EventArgs e)
        {
            LayoutMdi(MdiLayout.Cascade);
        }

        private void WindowTileMenuItem_Click(object sender, EventArgs e)
        {
            LayoutMdi(MdiLayout.TileHorizontal);
        }

        private void NewMenuItem_Click(object sender, EventArgs e)
        {
            ChildForm newChild = new()
            {
                MdiParent = this
            };
            newChild.Text = newChild.Text + " " + ++openDocuments;

            newChild.Show();
        }
    }
}
