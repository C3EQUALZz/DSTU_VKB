using FirstLaboratory.Core.Interfaces.FirstQuestion;


namespace FirstLaboratory.Presenters
{
    internal class FirstQuestionPresenter : IFirstQuestionPresenter
    {
        private readonly IFirstQuestionView _view;
        private readonly IFirstQuestionModel _model;

        public FirstQuestionPresenter(IFirstQuestionView view, IFirstQuestionModel model)
        {
            _view = view;
            _model = model;

            _view.BackgroundColor = _model.BackgroundColor;
        }

        public void OnResize(object sender, EventArgs e)
        {
            _model.Width = _view.Width;
            _model.Height = _view.Height;

            var path = new System.Drawing.Drawing2D.GraphicsPath();
            path.AddEllipse(0, 0, _view.Width, _view.Height);
            _view.Region = new Region(path);

            using var g = _view.CreateGraphics();
            _view.DrawEllipse(g, _model.BorderPen, _model.Width, _model.Height);
        }

        public void OnPaint(object sender, EventArgs e)
        {
            using var g = _view.CreateGraphics();
            _view.DrawEllipse(g, _model.BorderPen, _model.Width, _model.Height);
        }

        public void OnExitButtonClick(object sender, EventArgs e)
        {
            Application.Exit();
        }


    }
}
