﻿using DoAnPaint.Graphs.Core.Interfaces;

namespace DoAnPaint.Graphs.Models
{
    internal class FirstModel : IModel
    {
        public string Name => "y = x^2";

        public double Calculate(double x)
        {
            return x * x;
        }
    }
}
