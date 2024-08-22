using FirstLaboratory.Core.Interfaces.SecondQuestion;
using FirstLaboratory.Models;

namespace FirstLaboratory.Presenters
{
    internal class SecondQuestionSubPresenter : ISecondQuestionSubPresenter
    {
        private readonly ISecondQuestionSubView _view;
        private readonly ISecondQuestionModel _model;

        /// <summary>
        /// Презентер для 2 окна. Здесь решил описание формы (ромб) вынести в модель. 
        /// </summary>
        /// <param name="view">вьюшка для 2 окна в форме, которая должна быть в форме ромба</param>
        /// <param name="model">модель, где описывается сама форма ромба</param>
        public SecondQuestionSubPresenter(ISecondQuestionSubView view, SecondQuestionModel model)
        {
            _view = view;
            _model = model;
        }

        /// <summary>
        /// Метод презентера, который отрабатывает для загрузки окна в форме ромба
        /// </summary>
        public void OnLoad(object sender, EventArgs e)
        {
            _view.BackgroundColor = Color.Green;
            _view.SetRegion(new Region(_model.CreateDiamondPath(_view.Width, _view.Height)));
        }

        /// <summary>
        /// Метод презентера, который отрабатывает для выхода из приложения
        /// </summary>
        public void OnExitButtonClick(object sender, EventArgs e)
        {
            Application.Exit();
        }
    }
}
