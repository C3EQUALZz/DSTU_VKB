using DoAnPaint.Graphs.Core.Interfaces;
using System;

namespace DoAnPaint.Graphs.Models.FifthQuestion
{
    internal class FirstModel : IModel
    {
        public string Name => "y = 3 * sin(x)";

        public double Calculate(double x)
        {
            return 3 * Math.Sin(x);
        }
    }
}
