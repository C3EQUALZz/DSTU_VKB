namespace SecondLaboratory.Enums;

public class CalculatorOperationType
{
    public static CalculatorOperationType Eq = new("=");
    public static CalculatorOperationType Add = new("+");
    public static CalculatorOperationType Sub = new("-");
    public static CalculatorOperationType Mult = new("×");
    public static CalculatorOperationType Div = new("÷");

    public string Sign;

    private CalculatorOperationType(string sign)
    {
        Sign = sign;
    }
}
