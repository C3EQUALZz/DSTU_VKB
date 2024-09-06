using FirstLaboratory.Core.Interfaces.FirstQuestion;
using FirstLaboratory.Models;
using FirstLaboratory.Presenters;

namespace FirstLaboratory.Views
{
    /// <summary>
    /// Вьюшка для 1 задания 1 лабы
    /// </summary>
    public partial class FirstQuestionView : Form, IFirstQuestionView
    {
        private readonly IFirstQuestionPresenter _presenter;

        public FirstQuestionView()
        {
            _presenter = new FirstQuestionPresenter(this, new FirstQuestionModel());
            InitializeComponent();
        }

        public Color BackgroundColor
        {
            set => BackColor = value;
        }

        public new int Width => base.Width;
        public new int Height => base.Height;
        public new Region Region
        {
            set => base.Region = value;
        }

        /// <summary>
        /// Событие, которое установлено через Designer, здесь перерисовка для формы именно
        /// </summary>
        public void ResizeEvent(object sender, EventArgs e)
        {
            _presenter.OnResize(sender, e);
        }

        /// <summary>
        /// Нужно для презентера, чтобы перерисовать все
        /// </summary>
        public new Graphics CreateGraphics()
        {
            return base.CreateGraphics();
        }

        /// <summary>
        /// Событие, которое установлено через Designer, здесь отрисовка для формы именно
        /// </summary>
        public void PaintEvent(object sender, EventArgs e)
        {
            _presenter.OnPaint(sender, e);
        }

        /// <summary>
        /// Событие, которое установлено через Designer, здесь отработка для закрытия формы
        /// </summary>
        public void ExitButton_Click(object sender, EventArgs e)
        {
            _presenter.OnExitButtonClick(sender, e);
        }

        /// <summary>
        /// Метод, который рисует эллипс
        /// </summary>
        /// <param name="g"></param>
        /// <param name="borderPen">ширина эллипса</param>
        /// <param name="width">ширина эллипса</param>
        /// <param name="height">высота эллипса</param>
        public void DrawEllipse(Graphics g, Pen borderPen, int width, int height)
        {
            g.DrawEllipse(borderPen, 0, 0, width - 1, height - 1);
        }
    }
}
