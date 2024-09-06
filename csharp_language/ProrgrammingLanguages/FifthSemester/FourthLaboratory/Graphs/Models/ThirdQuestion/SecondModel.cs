using DoAnPaint.Graphs.Core.Interfaces;
using System;

namespace DoAnPaint.Graphs.Models.ThirdQuestion
{
    internal class SecondModel : IModel
    {
        public string Name => "y = 2 * exp(-x) + 3";

        public double Calculate(double x)
        {
            return 2 * Math.Exp(-x) + 3;
        }
    }
}
