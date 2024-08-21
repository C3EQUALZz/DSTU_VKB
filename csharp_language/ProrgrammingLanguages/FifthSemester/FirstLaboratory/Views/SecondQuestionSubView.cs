using FirstLaboratory.Core.Interfaces.SecondQuestion;
using FirstLaboratory.Presenters;
using FirstLaboratory.Models;

namespace FirstLaboratory
{
    public partial class SecondQuestionSubView : Form, ISecondQuestionSubView
    {
        private readonly ISecondQuestionSubPresenter _presenter;
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

        private Region? _region;

        public new Region Region
        {
            get { return _region; }
            set
            {
                _region = value;
                Invalidate();
            }
        }

        private void ExitButton_Click(object sender, EventArgs e)
        {
            _presenter.OnExitButtonClick(sender, e);
        }

        private void SecondForm_Load(object sender, EventArgs e)
        {
            _presenter.OnLoad(sender, e);
        }

        
    }
}
