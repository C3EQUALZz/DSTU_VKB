using DoAnPaint.Graphs.Core.Interfaces.FirstQuestion;

namespace DoAnPaint.Graphs.Models
{
    internal class SecondModel : IModel
    {
        public string Name => "y = -2(x - 1)^2 + 3";

        public double Calculate(double x)
        {
            return -2 * (x - 1) * (x - 1) + 3;
        }
    }
}
