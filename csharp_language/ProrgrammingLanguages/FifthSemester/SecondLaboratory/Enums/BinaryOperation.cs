using System;
using System.Collections.Generic;

namespace SecondLaboratory.Enums;

public class BinaryOperation
{
    public static BinaryOperation Add = new("+", (x, y) => x + y);
    public static BinaryOperation Sub = new("-", (x, y) => x - y);
    public static BinaryOperation Mult = new("×", (x, y) => x * y);
    public static BinaryOperation Div = new("÷", (x, y) => x / y);

    public string Sign;
    public Func<double, double, double> Run;

    public static List<BinaryOperation> All => 
    [
        Add,
        Sub,
        Mult,
        Div
    ];

    private BinaryOperation(string sign, Func<double, double, double> func)
    {
        Run = func;
        Sign = sign;
    }
}
