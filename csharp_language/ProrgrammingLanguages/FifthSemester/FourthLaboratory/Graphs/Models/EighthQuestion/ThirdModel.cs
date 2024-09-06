using DoAnPaint.Graphs.Core.Interfaces;
using System;

namespace DoAnPaint.Graphs.Models.EighthQuestion
{
    internal class ThirdModel : IModel
    {
        public string Name => "y = 1 / tan(x)";

        public double Calculate(double x)
        {
            return 1 / Math.Tan(x);
        }
    }
}
