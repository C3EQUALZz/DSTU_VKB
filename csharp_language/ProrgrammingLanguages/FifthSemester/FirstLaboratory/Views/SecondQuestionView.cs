using FirstLaboratory.Core.Interfaces.SecondQuestion;
using FirstLaboratory.Presenters;

namespace FirstLaboratory
{
    public partial class SecondQuestionView : Form, ISecondQuestionView
    {
        private readonly ISecondQuestionPresenter _presenter;

        public SecondQuestionView()
        {
            InitializeComponent();
            _presenter = new SecondQuestionPresenter(this);
        }

        public void ShowSecondForm()
        {
            new SecondQuestionSubView().Show();
        }

        public void SwapToSecondForm_Click(object sender, EventArgs e)
        {
            _presenter.OnSwapToSecondFormClick(sender, e);
        }
    }
}
