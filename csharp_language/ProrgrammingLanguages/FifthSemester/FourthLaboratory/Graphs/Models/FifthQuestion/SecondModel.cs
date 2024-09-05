using DoAnPaint.Graphs.Core.Interfaces;
using System;

namespace DoAnPaint.Graphs.Models.FifthQuestion
{
    internal class SecondModel : IModel
    {
        public string Name => "y = sin(2 * x)";

        public double Calculate(double x)
        {
            return Math.Sin(2 * x);
        }
    }
}
