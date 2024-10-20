using LiveCharts;
using LiveCharts.WinForms;

namespace DoAnPaint.Graphs.Core.Interfaces
{
    public interface IView
    {
        SeriesCollection ChartData { get; set; }
        CartesianChart CartesianChart { get; }
        double Step { get; set; }
        double Start { get; set; }
        double End { get; set; }
        bool IsAnimationEnabled { get; }
    }
}
