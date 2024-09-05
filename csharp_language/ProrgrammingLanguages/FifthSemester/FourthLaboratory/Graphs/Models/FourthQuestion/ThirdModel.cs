using DoAnPaint.Graphs.Core.Interfaces;
using System;

namespace DoAnPaint.Graphs.Models.FourthQuestion
{
    internal class ThirdModel : IModel
    {
        public string Name => "y = 2 * log5(x)";

        public double Calculate(double x)
        {
            return 2 * Math.Log(x, 5);
        }
    }
}
