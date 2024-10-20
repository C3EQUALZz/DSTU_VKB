using DoAnPaint.Graphs.Core.Interfaces;
using System;

namespace DoAnPaint.Graphs.Models.ThirdQuestion
{
    internal class FirstModel : IModel
    {
        public string Name => "y = 2 * exp(x)";

        public double Calculate(double x)
        {
            return 2 * Math.Exp(x);
        }
    }
}
