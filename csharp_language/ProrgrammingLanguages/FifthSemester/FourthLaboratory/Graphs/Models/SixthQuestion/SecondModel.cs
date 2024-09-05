using DoAnPaint.Graphs.Core.Interfaces;
using System;

namespace DoAnPaint.Graphs.Models.SixthQuestion
{
    internal class SecondModel : IModel
    {
        public string Name => "y = 5 * sin(3 * pi * x / 2 - pi / 2)";

        public double Calculate(double x)
        {
            return 5 * Math.Sin(3 * Math.PI * x / 2 - Math.PI / 2);
        }
    }
}
