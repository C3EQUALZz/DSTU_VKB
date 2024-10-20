using DoAnPaint.Graphs.Core.Interfaces;
using System;

namespace DoAnPaint.Graphs.Models.NinthQuestion
{
    internal class SecondModel : IModel
    {
        public string Name => "y = 1/(4 * sqrt(2pi)))*exp(-0.35(x-1))";

        public double Calculate(double x)
        {
            return 1 / (4 * Math.Sqrt(2)) * Math.Exp(-0.35 * (x - 1));
        }
    }
}
