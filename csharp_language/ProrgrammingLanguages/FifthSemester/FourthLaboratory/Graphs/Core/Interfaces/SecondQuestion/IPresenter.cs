namespace DoAnPaint.Graphs.Core.Interfaces.SecondQuestion
{
    internal interface IPresenter
    {
        void SelectModel(IModel model);
        void DeselectModel(IModel model);
        void Draw();
    }
}
