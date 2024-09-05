namespace DoAnPaint.Graphs.Core.Interfaces
{
    internal interface IModel
    {
        string Name { get; }

        double Calculate(double x);
    }
}
