using FirstLaboratory.Core.Interfaces.ThirdQuestion;
using FirstLaboratory.Presenters;

namespace FirstLaboratory.Views
{
    public partial class ThirdQuestionView : Form, IThirdQuestionView
    {
        private int openDocuments = 0;
        private MdiLayout _currentMdiLayout;
        private readonly IThirdQuestionPresenter _presenter;

        public ThirdQuestionView()
        {
            InitializeComponent();
            _presenter = new ThirdQuestionPresenter(this);
        }

        public MdiLayout MdiLayoutType
        {
            get => _currentMdiLayout;
            set
            {
                _currentMdiLayout = value;
                LayoutMdi(value);
            }
        }

        public void ExitMenuItem_Click(object sender, EventArgs e)
        {
            _presenter.OnExitMenuItem_Click(sender, e);
        }

        public void WindowCascadeMenuItem_Click(object sender, EventArgs e)
        {
            _presenter.OnWindowCascadeMenuItem_Click(sender, e);
        }

        public void WindowTileMenuItem_Click(object sender, EventArgs e)
        {
            _presenter.OnWindowTileMenuItem_Click(sender, e);
        }

        public void NewMenuItem_Click(object sender, EventArgs e)
        {
            ThirdQuestionSubView newChild = new()
            {
                MdiParent = this
            };
            newChild.Text = newChild.Text + " " + ++openDocuments;

            newChild.Show();
        }
    }
}
