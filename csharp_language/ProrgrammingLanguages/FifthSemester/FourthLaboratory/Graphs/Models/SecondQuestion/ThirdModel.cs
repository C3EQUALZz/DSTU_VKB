using DoAnPaint.Graphs.Core.Interfaces;

namespace DoAnPaint.Graphs.Models.SecondQuestion
{
    internal class ThirdModel : IModel
    {
        public string Name => "y = 1 / (2 * x)";

        public double Calculate(double x)
        {
            return 1 / (2 * x);
        }
    }
}
