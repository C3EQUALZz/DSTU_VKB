using SecondLaboratory.Enums;
using SecondLaboratory.Extensions;
using System;
using System.Windows.Forms;

namespace SecondLaboratory.Views.Calculator
{
    public partial class StandartCalculatorForm : Form
    {
        private string x = null;
        private string y = "0";
        private string result = null;
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
            ResultLabel.Text = "0";

            // NOT WORKING
            //RoundButtons();
        }

        private void ResetFlags()
        {
            calculated = false;
        }

        private void UpdateAll()
        {
            UpdateResult();
            UpdateOperation();
        }
        private void UpdateResult()
        {
            ResultLabel.Text = result;
        }
        private void UpdateOperation(bool showY = false)
        {
            OperationHistoryLabel.Text = $"{(x != null ? $"{x}" : "")}{(x != null && operation != null ? $" {operation.Sign}" : "")} {(showY ? y : "")}";
        }
        private void UpdateOperation(Func<string, string> modifyY)
        {
            OperationHistoryLabel.Text = $"{(x != null ? $"{x}" : "")}{(x != null && operation != null ? $" {operation.Sign}" : "")} {modifyY(y)}";
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
            if (x != null && operation != null)
            {
                x = operation.Run(double.Parse(x), double.Parse(y)).ToString();
                result = x;
                calculated = true;
            }
        }

        private void DigitButton_Click(object sender, System.EventArgs e)
        {
            if (calculated)
            {
                y = "0";
                ResetFlags();
            }

            var digit = (sender as Button).Text;

            if (digit == "," && result != null && result.Contains(","))
            {
                return;
            }

            if (y == "0" && digit != ",")
            {
                y = null;
            }

            y += digit;
            result = y;

            UpdateResult();
        }
        private void BackspaceButton_Click(object sender, System.EventArgs e)
        {
            if (calculated)
            {
                x = null;
                operation = null;

                UpdateAll();
                ResetFlags();
                return;
            }

            if (y == null) return;

            if (y != "0")
            {
                y = y.Substring(0, y.Length - 1);

                if (y.Length < 1)
                {
                    y = "0";
                }

                result = y;
            }

            UpdateResult();
        }
        private void EqualsButton_Click(object sender, System.EventArgs e)
        {
            if (y == null)
            {
                y = x;
            }
            UpdateOperation(x => $"{x} =");
            Calculate();
            UpdateResult();
        }
        
        private void BinaryOperation_Click(object sender, System.EventArgs e)
        {
            var change = y == null && operation != null;

            if (!change) Calculate();

            operation = BinaryOperation.All.Find(o => o.Sign == (sender as Button).Text);
            
            if (change)
            {
                UpdateOperation();
                return;
            }
            
            if (!calculated) x = y;

            UpdateAll();

            y = null;
        }
        private void UnaryOperation_Click(object sender, System.EventArgs e)
        {
            var op = UnaryOperation.All.Find(o => o.Sign == (sender as Button).Text);
            UpdateOperation(op.Modify);
            result = op.Run(double.Parse(y)).ToString();
            y = result;
            UpdateResult();
        }
        
        private void NegateButton_Click(object sender, System.EventArgs e)
        {
            if (y != null)
            {
                if (y[0] == '-')
                {
                    result = y.Substring(1);
                }
                else if (y != "0")
                {
                    result = '-' + y;
                }

                UpdateOperation(x => $"negate({x})");
                UpdateResult();

                y = result;
            }
        }
        private void PercentButton_Click(object sender, System.EventArgs e)
        {
            if (x != null)
            {
                y = (double.Parse(x) / 100 * double.Parse(y)).ToString();
                result = y;
                UpdateResult();
                UpdateOperation(true);
            }
        }
        
        private void CButton_Click(object sender, System.EventArgs e)
        {
            x = null;
            operation = null;
            y = "0";
            result = y;

            UpdateAll();
        }
        private void CEButton_Click(object sender, System.EventArgs e)
        {
            if (calculated)
            {
                operation = null;
                x = null;
                UpdateOperation();
            }

            y = "0";
            result = y;
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
            y = memoryCell.ToString();
            result = y;
            UpdateAll();
        }
        private void MSButton_Click(object sender, System.EventArgs e)
        {
            if (y == null) return;

            memoryCell = double.Parse(y);

            MCButton.Enabled = true;
            MRButton.Enabled = true;
        }
        private void MPButton_Click(object sender, System.EventArgs e)
        {
            if (y == null) return;

            if (memoryCell == null)
            {
                MSButton_Click(sender, e);
                return;
            }

            memoryCell += double.Parse(y);
        }
        private void MMButton_Click(object sender, System.EventArgs e)
        {
            if (y == null) return;

            if (memoryCell == null)
            {
                MSButton_Click(sender, e);
                return;
            }

            memoryCell -= double.Parse(y);
        }
    }
}
