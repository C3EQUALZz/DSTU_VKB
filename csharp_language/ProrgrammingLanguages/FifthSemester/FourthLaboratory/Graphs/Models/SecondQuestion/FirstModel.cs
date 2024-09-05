using DoAnPaint.Graphs.Core.Interfaces.SecondQuestion;

namespace DoAnPaint.Graphs.Models.SecondQuestion
{
    internal class FirstModel : IModel
    {
        public string Name => "y = 2 / x";

        public double Calculate(double x)
        {
            return 2 / x;
        }

    }
}
