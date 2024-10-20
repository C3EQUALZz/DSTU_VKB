using DoAnPaint.Graphs.Core.Interfaces;
using System;

namespace DoAnPaint.Graphs.Models.FifthQuestion
{
    internal class ThirdModel : IModel
    {
        public string Name => "y = sin(x) + 0.5";

        public double Calculate(double x)
        {
            return Math.Sin(x) + 0.5;
        }
    }
}
