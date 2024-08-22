using FirstLaboratory.Core.Interfaces.SecondQuestion;
using FirstLaboratory.Presenters;

namespace FirstLaboratory
{
    public partial class SecondQuestionView : Form, ISecondQuestionView
    {
        private readonly ISecondQuestionPresenter _presenter;

        /// <summary>
        /// View в паттерне MVP для 2 задания (главное окно - стартовое)
        /// </summary>
        public SecondQuestionView()
        {
            InitializeComponent();
            _presenter = new SecondQuestionPresenter(this);
        }

        /// <summary>
        /// Переключение на вторую форму, которую просили в задании
        /// </summary>
        public void ShowSecondForm()
        {
            new SecondQuestionSubView().Show();
        }

        /// <summary>
        /// Обработчик клика для переключения на 2 форму
        /// </summary>
        public void SwapToSecondForm_Click(object sender, EventArgs e)
        {
            _presenter.OnSwapToSecondFormClick(sender, e);
        }
    }
}
