using DoAnPaint.Graphs.Core.Interfaces;
using System;

namespace DoAnPaint.Graphs.Models.TenthQuestion
{
    internal class FirstModel : IModel
    {

        public string Name => "y = sec(x)";

        public double Calculate(double x)
        {
            return Sec(x);
        }

        private static double Sec(double x)
        {
            return 1 / Math.Cos(x);
        }

        

    }
}
