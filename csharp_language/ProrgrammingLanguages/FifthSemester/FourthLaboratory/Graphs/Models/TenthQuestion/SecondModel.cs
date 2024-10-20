using DoAnPaint.Graphs.Core.Interfaces;
using System;

namespace DoAnPaint.Graphs.Models.TenthQuestion
{
    internal class SecondModel : IModel
    {
        public string Name => "y = 2 * sec(x) - 1";

        public double Calculate(double x)
        {
            return 2 * Sec(x) - 1;
        }

        private static double Sec(double x)
        {
            return 1 / Math.Cos(x);
        }

    }
}
