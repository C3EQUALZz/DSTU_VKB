using System.Collections.Generic;
using System;

namespace SecondLaboratory.Enums;

public class UnaryOperation
{
    public static UnaryOperation Inv = new("1/x", (x) => 1 / x, x => $"1/({x})");
    public static UnaryOperation Square = new("x²", (x) => x * x, x => $"sqr({x})");
    public static UnaryOperation SquareRoot = new("√x", Math.Sqrt, x => $"sqrt({x})");

    public string Sign;
    public Func<double, double> Run;
    public Func<string, string> Modify;

    public static List<UnaryOperation> All =>
    [
        Inv,
        Square,
        SquareRoot
    ];

    private UnaryOperation(string sign, Func<double, double> func, Func<string, string> modify)
    {
        Run = func;
        Sign = sign;
        Modify = modify;
    }
}
