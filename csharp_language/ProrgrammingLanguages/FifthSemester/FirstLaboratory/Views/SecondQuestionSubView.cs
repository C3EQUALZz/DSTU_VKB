using FirstLaboratory.Core.Interfaces.SecondQuestion;
using FirstLaboratory.Presenters;
using FirstLaboratory.Models;

namespace FirstLaboratory
{
    public partial class SecondQuestionSubView : Form, ISecondQuestionSubView
    {
        private readonly ISecondQuestionSubPresenter _presenter;

        /// <summary>
        /// 2 окно, на которое нам нужно переключиться, опять-таки тот же самый View в паттрене MVP для 2 окна
        /// </summary>
        public SecondQuestionSubView()
        {
            InitializeComponent();
            _presenter = new SecondQuestionSubPresenter(this, new SecondQuestionModel());
        }

        public new int Width => base.Width;
        public new int Height => base.Height;

        public Color BackgroundColor
        {
            set => BackColor = value;
        }

        /// <summary>
        /// Обработчик нажатия на кнопку ExitButton, который установлен через Designer 
        /// </summary>
        public void ExitButton_Click(object sender, EventArgs e)
        {
            _presenter.OnExitButtonClick(sender, e);
        }

        /// <summary>
        /// Обработчик на загрузку формы, который установлен через Designer
        /// </summary>
        public void SecondForm_Load(object sender, EventArgs e)
        {
            _presenter.OnLoad(sender, e);
        }

        /// <summary>
        /// Здесь использую сеттер вместо свойства, потому что не отрабатывает свойство. 
        /// Скорее всего модификатор new там все ломает, хотя я не понимаю почему, особенности C#. 
        /// </summary>
        /// <param name="region"></param>
        public void SetRegion(Region region)
        {
            Region = region;
        }


    }
}
