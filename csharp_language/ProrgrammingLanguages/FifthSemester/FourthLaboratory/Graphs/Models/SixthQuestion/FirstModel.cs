using DoAnPaint.Graphs.Core.Interfaces;
using System;

namespace DoAnPaint.Graphs.Models.SixthQuestion
{
    internal class FirstModel : IModel
    {
        public string Name => "y = 3 * sin(2*pi*x + pi / 4)";

        public double Calculate(double x)
        {
            return 3 * Math.Sin(2 * Math.PI * x + Math.PI / 4);
        }
    }
}
