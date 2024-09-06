using DoAnPaint.Graphs.Core.Interfaces;
using System;

namespace DoAnPaint.Graphs.Models.EighthQuestion
{
    internal class SecondModel : IModel
    {
        public string Name => "y = tan(x - pi / 4)";

        public double Calculate(double x)
        {
            return Math.Tan(x - Math.PI / 4);
        }
    }
}
