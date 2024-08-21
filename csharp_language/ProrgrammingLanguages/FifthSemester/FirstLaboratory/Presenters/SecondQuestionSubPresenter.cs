using FirstLaboratory.Core.Interfaces.SecondQuestion;
using FirstLaboratory.Models;

namespace FirstLaboratory.Presenters
{
    internal class SecondQuestionSubPresenter : ISecondQuestionSubPresenter
    {
        private readonly ISecondQuestionSubView _view;
        private readonly ISecondQuestionModel _model;

        public SecondQuestionSubPresenter(ISecondQuestionSubView view, SecondQuestionModel model)
        {
            _view = view;
            _model = model;
        }

        public void OnLoad(object sender, EventArgs e)
        {
            _view.BackgroundColor = Color.Green;
            _view.Region = new Region(_model.CreateDiamondPath(_view.Width, _view.Height));
        }

        public void OnExitButtonClick(object sender, EventArgs e)
        {
            Application.Exit();
        }
    }
}
