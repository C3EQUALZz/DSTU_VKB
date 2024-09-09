using System.Collections.Generic;
using System;

namespace SecondLaboratory.Enums;

public class UnaryOperation
{
    public static UnaryOperation Inv = new("1/x", (x) => 1 / x);
    public static UnaryOperation Square = new("x²", (x) => x * x);
    public static UnaryOperation SquareRoot = new("√x", Math.Sqrt);

    public string Sign;
    public Func<double, double> Run;

    public static List<UnaryOperation> All =>
    [
        Inv,
        Square,
        SquareRoot
    ];

    private UnaryOperation(string sign, Func<double, double> func)
    {
        Run = func;
        Sign = sign;
    }
}
