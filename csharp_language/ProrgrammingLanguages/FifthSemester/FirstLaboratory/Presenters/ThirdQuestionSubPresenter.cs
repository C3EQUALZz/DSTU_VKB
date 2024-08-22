using FirstLaboratory.Core.Interfaces.ThirdQuestion;

namespace FirstLaboratory.Presenters
{
    internal class ThirdQuestionSubPresenter : IThirdQuestionSubPresenter
    {
        private readonly IThirdQuestionSubView _view;

        public ThirdQuestionSubPresenter(IThirdQuestionSubView view)
        {
            _view = view;
        }

        public void ToggleMenuItemClick(object sender, EventArgs e)
        {
            if (_view.ToggleMenuItemChecked)
            {
                _view.ToggleMenuItemChecked = false;
                _view.ChildTextBoxForeColor = Color.Black;
            }
            else
            {
                _view.ToggleMenuItemChecked = true;
                _view.ChildTextBoxForeColor = Color.Blue;
            }
        }
    }
}
