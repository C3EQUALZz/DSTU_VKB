using DoAnPaint.Graphs.Core.Interfaces;
using System;

namespace DoAnPaint.Graphs.Models.ThirdQuestion
{
    internal class ThirdModel : IModel
    {
        public string Name => "y = exp(x) - 1";

        public double Calculate(double x)
        {
            return Math.Exp(x) - 1;
        }
    }
}
