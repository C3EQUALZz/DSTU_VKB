using FirstLaboratory.Core.Interfaces.SecondQuestion;

namespace FirstLaboratory.Presenters
{
    internal class SecondQuestionPresenter : ISecondQuestionPresenter
    {
        private readonly ISecondQuestionView _view;

        public SecondQuestionPresenter(ISecondQuestionView view)
        {
            _view = view;
        }

        public void OnSwapToSecondFormClick(object sender, EventArgs e)
        {
            _view.ShowSecondForm();
            _view.Hide();
        }

    }
}
