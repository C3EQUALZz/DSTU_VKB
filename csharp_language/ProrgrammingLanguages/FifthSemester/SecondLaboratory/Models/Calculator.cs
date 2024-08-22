namespace SecondLaboratory.Models;

public class CalculatorModel
{
    public double Evaluate(double a, double b, string operation)
    {
        return operation switch
        {
            "+" => Add(a, b),
            "-" => Subtract(a, b),
            "×" => Multiply(a, b),
            "÷" => Divide(a, b),
            _ => throw new InvalidOperationException("Invalid operation")
        };
    }

    public double Evaluate(double a, string operation)
    {
        return operation switch
        {
            "√𝑥" => SquareRoot(a),
            "𝑥²" => Square(a),
            "⅟𝑥" => Reciprocal(a),
            "%" => Percent(a),
            "±" => Negate(a),
            _ => throw new InvalidOperationException("Invalid operation")
        };
    }

    public static double Add(double a, double b) => a + b;
    public static double Subtract(double a, double b) => a - b;
    public static double Multiply(double a, double b) => a * b;
    public static double Divide(double a, double b)
    {
        if (b == 0)
            throw new DivideByZeroException("Division by zero is not allowed.");
        return a / b;
    }

    public static double SquareRoot(double a) => Math.Sqrt(a);
    public static double Square(double a) => a * a;
    public static double Reciprocal(double a)
    {
        if (a == 0)
            throw new DivideByZeroException("Division by zero is not allowed.");
        return 1.0 / a;
    }

    public static double Percent(double a) => a / 100;
    public static double Negate(double a) => -a;
}
