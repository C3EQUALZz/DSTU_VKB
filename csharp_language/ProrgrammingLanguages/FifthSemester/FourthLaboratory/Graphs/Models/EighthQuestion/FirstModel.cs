using DoAnPaint.Graphs.Core.Interfaces;
using System;

namespace DoAnPaint.Graphs.Models.EighthQuestion
{
    internal class FirstModel : IModel
    {
        public string Name => "y = 2 * tan(x)";

        public double Calculate(double x)
        {
            return 2 * Math.Tan(x);
        }
    }
}
