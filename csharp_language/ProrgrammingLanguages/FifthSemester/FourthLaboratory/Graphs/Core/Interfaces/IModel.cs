namespace DoAnPaint.Graphs.Core.Interfaces
{
    public interface IModel
    {
        string Name { get; }

        double Calculate(double x);
    }
}
