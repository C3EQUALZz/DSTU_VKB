using FirstLaboratory.Core.Interfaces.ThirdQuestion;
using FirstLaboratory.Presenters;

namespace FirstLaboratory.Views
{
    public partial class ThirdQuestionSubView : Form, IThirdQuestionSubView
    {
        private readonly IThirdQuestionSubPresenter _presenter;

        public ThirdQuestionSubView()
        {
            InitializeComponent();
            _presenter = new ThirdQuestionSubPresenter(this);
        }

        public bool ToggleMenuItemChecked
        {
            get => ToggleMenuItem.Checked;
            set => ToggleMenuItem.Checked = value;
        }

        public Color ChildTextBoxForeColor
        {
            get => ChildTextBox.ForeColor;
            set => ChildTextBox.ForeColor = value;
        }

        public void ToggleMenuItem_Click(object sender, EventArgs e)
        {
            _presenter.ToggleMenuItemClick(sender, e);
        }
    }
}
