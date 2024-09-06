using DoAnPaint.Graphs.Core.Interfaces;
using System;

namespace DoAnPaint.Graphs.Models.TenthQuestion
{
    internal class ThirdModel : IModel
    {
        public string Name => "y = sec(2x)";

        public double Calculate(double x)
        {
            return Sec(2 * x);
        }

        private static double Sec(double x)
        {
            return 1 / Math.Cos(x);
        }

    }
}
