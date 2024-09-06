using DoAnPaint.Graphs.Core.Interfaces;
using System;

namespace DoAnPaint.Graphs.Models.NinthQuestion
{
    internal class ThirdModel : IModel
    {
        public string Name => "y = (3 / (2 * sqrt(2pi))) * exp(-0.35 * (x+2))";

        public double Calculate(double x)
        {
            return 3 / (2 * Math.Sqrt(2 * Math.PI)) * Math.Exp(-0.35 * (x + 2));
        }
    }
}
