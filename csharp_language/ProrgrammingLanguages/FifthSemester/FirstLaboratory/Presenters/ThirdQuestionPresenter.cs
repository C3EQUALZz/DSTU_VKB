using FirstLaboratory.Core.Interfaces.ThirdQuestion;

namespace FirstLaboratory.Presenters
{
    internal class ThirdQuestionPresenter : IThirdQuestionPresenter
    {
        private readonly IThirdQuestionView _view;

        public ThirdQuestionPresenter(IThirdQuestionView view)
        {
            _view = view;
        }

        public void OnExitMenuItem_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        public void OnWindowCascadeMenuItem_Click(object sender, EventArgs e)
        {
            _view.MdiLayoutType = MdiLayout.Cascade;
        }

        public void OnWindowTileMenuItem_Click(object sender, EventArgs e)
        {
            _view.MdiLayoutType = MdiLayout.TileHorizontal;
        }

    }
}
