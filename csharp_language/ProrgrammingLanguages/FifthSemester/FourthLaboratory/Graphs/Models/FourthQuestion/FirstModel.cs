using DoAnPaint.Graphs.Core.Interfaces;
using System;

namespace DoAnPaint.Graphs.Models.FourthQuestion
{
    internal class FirstModel : IModel
    {
        public string Name => "y = log2(x)";

        public double Calculate(double x)
        {
            return Math.Log(x, 2);
        }
    }
}
