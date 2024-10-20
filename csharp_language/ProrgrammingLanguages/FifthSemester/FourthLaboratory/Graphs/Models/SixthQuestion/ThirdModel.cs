using DoAnPaint.Graphs.Core.Interfaces;
using System;

namespace DoAnPaint.Graphs.Models.SixthQuestion
{
    internal class ThirdModel : IModel
    {
        public string Name => "y = 4 * sin(pi * x / 3 + pi / 6)";

        public double Calculate(double x)
        {
            return 4 * Math.Sin(Math.PI * x / 3 + Math.PI / 6);
        }
    }
}
