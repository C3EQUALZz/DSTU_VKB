using FirstLaboratory.Core.Interfaces.FirstQuestion;
using FirstLaboratory.Models;
using FirstLaboratory.Presenters;

namespace FirstLaboratory.Views
{
    public partial class FirstQuestionView : Form, IFirstQuestionView
    {
        private readonly IFirstQuestionPresenter _presenter;

        public FirstQuestionView()
        {
            InitializeComponent();
            _presenter = new FirstQuestionPresenter(this, new FirstQuestionModel());
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

        public void ResizeEvent(object sender, EventArgs e)
        {
            _presenter.OnResize(sender, e);
        }

        public new Graphics CreateGraphics()
        {
            return base.CreateGraphics();
        }

        public void PaintEvent(object sender, EventArgs e)
        {
            _presenter.OnPaint(sender, e);
        }

        public void ExitButton_Click(object sender, EventArgs e)
        {
            _presenter.OnExitButtonClick(sender, e);
        }

        public void DrawEllipse(Graphics g, Pen borderPen, int width, int height)
        {
            g.DrawEllipse(borderPen, 0, 0, width - 1, height - 1);
        }
    }
}
