using DoAnPaint.Graphs.Core.Interfaces;

namespace DoAnPaint.Graphs.Models.SecondQuestion
{
    internal class SecondModel : IModel
    {
        public string Name => "y = - 3 / x";

        public double Calculate(double x)
        {
            return -3 / x;
        }
    }
}
