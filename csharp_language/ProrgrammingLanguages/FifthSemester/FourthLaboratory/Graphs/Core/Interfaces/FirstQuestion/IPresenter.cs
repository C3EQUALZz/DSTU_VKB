namespace DoAnPaint.Graphs.Core.Interfaces.FirstQuestion
{
    internal interface IPresenter
    {
        void SelectModel(IModel model);
        void DeselectModel(IModel model);
        void Draw();
    }
}
