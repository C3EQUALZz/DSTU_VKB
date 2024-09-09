using SecondLaboratory.Enums;
using SecondLaboratory.Extensions;
using System.Windows.Forms;

namespace SecondLaboratory.Views.Calculator
{
    public partial class StandartCalculatorForm : Form
    {
        private string lastNumber = null;
        private string number = "0";
        private BinaryOperation operation = null;

        public StandartCalculatorForm()
        {
            InitializeComponent();
        }

        private void StandartCalculatorForm_Load(object sender, System.EventArgs e)
        {
            OperationHistoryLabel.Text = string.Empty;
            OperationLabel.Text = "0";

            // NOT WORKING
            //RoundButtons();
        }



        private void UpdateUI()
        {
            OperationLabel.Text = number;

            if (operation != null && lastNumber != null)
            {
                OperationHistoryLabel.Text = $"{lastNumber} {operation.Sign}";
            }
            else
            {
                OperationHistoryLabel.Text = string.Empty;
            }
        }

        // HELP
        private void RoundButtons()
        {
            Button[] buttons = [
                    PercentButton,
                    CEButton,
                    CButton,
                    BackspaceButton,
                    InvertButton,
                    SquareButton,
                    SquareRootButton,
                    DivisionButton,
                    SevenButton,
                    EightButton,
                    NineButton,
                    MultiplicationButton,
                    FourButton,
                    FiveButton,
                    SixButton,
                    MinusButton,
                    OneButton,
                    TwoButton,
                    ThreeButton,
                    PlusButton,
                    PMButton,
                    ZeroButton,
                    PointButton,
                    EqualsButton
            ];

            foreach (var button in buttons)
            {
                button.SetRoundedShape(10);
            }
        }

        private void Calculate()
        {
            if (lastNumber != null && operation != null)
            {
                number = operation.Run(double.Parse(lastNumber), double.Parse(number)).ToString();
                lastNumber = null;
            }
        }

        private void DigitButton_Click(object sender, System.EventArgs e)
        {
            var digit = (sender as Button).Text;

            if (number == "0" && digit != ",")
            {
                number = string.Empty;
            }

            number += digit;

            UpdateUI();
        }

        private void BackspaceButton_Click(object sender, System.EventArgs e)
        {
            if (number != "0")
            {
                number = number.Substring(0, number.Length - 1);

                if (number.Length < 1)
                {
                    number = "0";
                }
            }

            UpdateUI();
        }

        private void EqualsButton_Click(object sender, System.EventArgs e)
        {
            if (operation != null && lastNumber != null)
            {
                OperationHistoryLabel.Text = $"{lastNumber} {operation.Sign} {number} =";
            }
            else
            {
                OperationHistoryLabel.Text = $"{number} =";
            }

            Calculate();

            OperationLabel.Text = number;
        }

        private void BinaryOperation_Click(object sender, System.EventArgs e)
        {
            Calculate();

            lastNumber = number;

            operation = BinaryOperation.All.Find(o => o.Sign == (sender as Button).Text);

            UpdateUI();

            number = "0";
        }

        private void NegateButton_Click(object sender, System.EventArgs e)
        {
            if (number[0] == '-')
            {
                number = number.Substring(1);
            }
            else if (number != "0")
            {
                number = '-' + number;
            }

            UpdateUI();
        }

        private void CButton_Click(object sender, System.EventArgs e)
        {
            lastNumber = null;
            operation = null;
            number = "0";

            UpdateUI();
        }

        private void CEButton_Click(object sender, System.EventArgs e)
        {
            number = "0";

            UpdateUI();
        }

        private void PercentButton_Click(object sender, System.EventArgs e)
        {
            if (lastNumber != null)
            {
                number = (double.Parse(lastNumber) / 100 * double.Parse(number)).ToString();
                UpdateUI();
                OperationHistoryLabel.Text += $" {number}";
            }
        }
    }
}
