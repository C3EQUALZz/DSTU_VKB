namespace DoAnPaint.Graphs.Core.Interfaces
{
    public interface IPresenter
    {
        void SelectModel(IModel model);
        void DeselectModel(IModel model);
        void Draw();
    }
}
