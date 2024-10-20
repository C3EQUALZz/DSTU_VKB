using DoAnPaint.Graphs.Core.Interfaces;
using System;

namespace DoAnPaint.Graphs.Models.SeventhQuestion
{
    internal class FirstModel : IModel
    {
        public string Name => "y = 2 * cos(3x - pi / 4)";

        public double Calculate(double x)
        {
            return 2 * Math.Cos(3 * x - Math.PI / 4);
        }

    }
}
