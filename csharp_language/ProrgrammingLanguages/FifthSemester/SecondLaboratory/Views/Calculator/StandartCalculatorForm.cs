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

        private double? memoryCell = null;
        private bool calculated = false;

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

        private void UpdateAll()
        {
            UpdateNumber();
            UpdateOperation();
        }

        private void UpdateNumber()
        {
            OperationLabel.Text = number;
        }

        private void ResetFlags()
        {
            calculated = false;
        }

        private void UpdateOperation(bool showNumber = false, string end = "")
        {
            OperationHistoryLabel.Text = $"{(lastNumber != null ? $"{lastNumber}" : "")}{(lastNumber != null && operation != null ? $" {operation.Sign}" : "")} {(showNumber ? number : "")}{end}";
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
                calculated = true;
            }
        }

        private void DigitButton_Click(object sender, System.EventArgs e)
        {
            if (calculated)
            {
                number = "0";
                ResetFlags();
            }

            var digit = (sender as Button).Text;

            if (number == "0" && digit != ",")
            {
                number = string.Empty;
            }

            number += digit;

            UpdateNumber();
        }
        private void BackspaceButton_Click(object sender, System.EventArgs e)
        {
            if (calculated)
            {
                UpdateAll();
                ResetFlags();
                return;
            }

            if (number != "0")
            {
                number = number.Substring(0, number.Length - 1);

                if (number.Length < 1)
                {
                    number = "0";
                }
            }

            UpdateNumber();
        }
        private void EqualsButton_Click(object sender, System.EventArgs e)
        {
            UpdateOperation(true, " =");
            Calculate();
            UpdateNumber();
        }
        
        private void BinaryOperation_Click(object sender, System.EventArgs e)
        {
            Calculate();

            operation = BinaryOperation.All.Find(o => o.Sign == (sender as Button).Text);
            lastNumber = number;

            UpdateAll();

            number = "0";
        }
        private void UnaryOperation_Click(object sender, System.EventArgs e)
        {
            number = UnaryOperation.All.Find(o => o.Sign == (sender as Button).Text).Run(double.Parse(number)).ToString();
            UpdateNumber();
            UpdateOperation(true);
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

            UpdateAll();
        }
        private void PercentButton_Click(object sender, System.EventArgs e)
        {
            if (lastNumber != null)
            {
                number = (double.Parse(lastNumber) / 100 * double.Parse(number)).ToString();
                UpdateNumber();
                UpdateOperation(true);
            }
        }
        
        private void CButton_Click(object sender, System.EventArgs e)
        {
            lastNumber = null;
            operation = null;
            number = "0";

            UpdateAll();
        }
        private void CEButton_Click(object sender, System.EventArgs e)
        {
            number = "0";
            UpdateAll();
        }
        
        private void MCButton_Click(object sender, System.EventArgs e)
        {
            memoryCell = null;

            MCButton.Enabled = false;
            MRButton.Enabled = false;
        }
        private void MRButton_Click(object sender, System.EventArgs e)
        {
            number = memoryCell.ToString();
            UpdateAll();
        }
        private void MSButton_Click(object sender, System.EventArgs e)
        {
            memoryCell = double.Parse(number);

            MCButton.Enabled = true;
            MRButton.Enabled = true;
        }
        private void MPButton_Click(object sender, System.EventArgs e)
        {
            if (memoryCell == null)
            {
                MSButton_Click(sender, e);
                return;
            }

            memoryCell += double.Parse(number);
        }
        private void MMButton_Click(object sender, System.EventArgs e)
        {
            if (memoryCell == null)
            {
                MSButton_Click(sender, e);
                return;
            }

            memoryCell -= double.Parse(number);
        }
    }
}
