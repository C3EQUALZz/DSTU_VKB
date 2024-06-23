using WinFormsAppForLaboratories.Laboratories.SecondLaboratory.Core.Classes;

namespace WinFormsAppForLaboratories.Laboratories.SecondLaboratory.Views;

public partial class CalculatorView : Form
{

    private bool enterValue = false;
    private string operation = string.Empty;
    private string? firstNumber, secondNumber;
    Double result = 0;

    public CalculatorView()
    {
        InitializeComponent();
    }

    private void OnButtonNumberClick(object sender, EventArgs e)
    {
        enterValue = false;
        var button = (CustomButton)sender;

        if (textDisplay1.Text == "0" || enterValue)
        {
            textDisplay1.Text = string.Empty;
        }


        if ((button.Text == "." && !textDisplay1.Text.Contains('.')) || button.Text != ".")
        {
            textDisplay1.Text += button.Text;
        }


    }

    private void OnButtonMathOperationClick(object sender, EventArgs e)
    {
        if (result != 0)
        {
            buttonEquals.PerformClick();
        }

        else
        {
            result = Double.Parse(textDisplay1.Text);
        }

        var button = (CustomButton)sender;
        operation = button.Text;
        enterValue = true;
        if (textDisplay1.Text != "0")
        {
            textDisplay2.Text = firstNumber = $"{result} {operation}";
            textDisplay1.Text = string.Empty;
        }
    }

    private void OnButtonEqualsClick(object sender, EventArgs e)
    {
        secondNumber = textDisplay1.Text;
        textDisplay2.Text = $"{textDisplay2.Text} {textDisplay1.Text}=";

        if (textDisplay1.Text != string.Empty)
        {
            if (textDisplay1.Text == "0")
                textDisplay2.Text = string.Empty;

            textDisplay1.Text = operation switch
            {
                "+" => (result + Double.Parse(textDisplay1.Text)).ToString(),
                "-" => (result - Double.Parse(textDisplay1.Text)).ToString(),
                "×" => (result * Double.Parse(textDisplay1.Text)).ToString(),
                "÷" => (result / Double.Parse(textDisplay1.Text)).ToString(),
                _ => $"{textDisplay1.Text} = ",
            };

            richTextBoxDisplayHistory.AppendText($"{firstNumber} {secondNumber} = {textDisplay1.Text}");
        }
    }

    private void OnClickButtonHistory(object sender, EventArgs e)
    {
        panelHistory.Height = (panelHistory.Height == 5) ? 355 : 5;
    }

   
}
