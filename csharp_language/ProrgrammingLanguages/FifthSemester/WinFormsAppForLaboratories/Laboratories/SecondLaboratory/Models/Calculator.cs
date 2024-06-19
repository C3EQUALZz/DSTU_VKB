using NCalc;

namespace WinFormsAppForLaboratories.Laboratories.SecondLaboratory.Models;

public class CalculatorModel
{
    public static double Evaluate(string expression)
    {
        return Convert.ToDouble(new Expression(expression).Evaluate());
    }
}
