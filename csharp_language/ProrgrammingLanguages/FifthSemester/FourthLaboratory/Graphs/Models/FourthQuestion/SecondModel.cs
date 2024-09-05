using DoAnPaint.Graphs.Core.Interfaces;
using System;

namespace DoAnPaint.Graphs.Models.FourthQuestion
{
    internal class SecondModel : IModel
    {
        public string Name => "y = log3(x + 1)";

        public double Calculate(double x)
        {
            return Math.Log(x + 1, 3);
        }
    }
}
