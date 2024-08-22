using FirstLaboratory.Core.Interfaces.SecondQuestion;

namespace FirstLaboratory.Presenters
{
    internal class SecondQuestionPresenter : ISecondQuestionPresenter
    {
        private readonly ISecondQuestionView _view;

        /// <summary>
        /// Презентер для главного - стартового окна 2 задания.
        /// Здесь не передается модель, потому что её нет. Ну нам нужно переключиться только на 2 окно
        /// </summary>
        /// <param name="view">вьюшка главного окна 2 задания</param>
        public SecondQuestionPresenter(ISecondQuestionView view)
        {
            _view = view;
        }

        /// <summary>
        /// Метод в презентере, который запускает обработку переключения на вторую форму, закрывая 1 форму.
        /// На всякий случай здесь Application.Exit() нельзя, потому что нам нужно закрыть форму, а не все приложение. 
        /// </summary>
        public void OnSwapToSecondFormClick(object sender, EventArgs e)
        {
            _view.ShowSecondForm();
            _view.Hide();
        }

    }
}
