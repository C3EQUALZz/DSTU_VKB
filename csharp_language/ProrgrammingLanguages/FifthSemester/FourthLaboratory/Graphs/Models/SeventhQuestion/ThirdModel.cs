using DoAnPaint.Graphs.Core.Interfaces;
using System;

namespace DoAnPaint.Graphs.Models.SeventhQuestion
{
    internal class ThirdModel : IModel
    {
        public string Name => "y = 3 * cos(x / 2 + pi / 2)";

        public double Calculate(double x)
        {
            return 3 * Math.Cos(x / 2 + Math.PI / 2);
        }
    }
}
