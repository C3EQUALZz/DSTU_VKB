using DoAnPaint.Graphs.Core.Interfaces.FirstQuestion;

namespace DoAnPaint.Graphs.Models.FirstQuestion
{
    internal class ThirdModel : IModel
    {

        public string Name => "y = (1/3)(x + 2)^2 - 4";

        public double Calculate(double x)
        {
            return (1.0 / 3) * (x + 2) * (x + 2) - 4;
        }
    }
}
