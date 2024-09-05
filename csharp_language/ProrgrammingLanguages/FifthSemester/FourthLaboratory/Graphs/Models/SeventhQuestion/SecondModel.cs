using DoAnPaint.Graphs.Core.Interfaces;
using System;

namespace DoAnPaint.Graphs.Models.SeventhQuestion
{
    internal class SecondModel : IModel
    {
        public string Name => "y = 1.5 * cos(2*x + pi / 3)";

        public double Calculate(double x)
        {
            return 1.5 * Math.Cos(2 * x + Math.PI / 3);
        }
    }
}
