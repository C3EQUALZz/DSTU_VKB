using SecondLaboratory.Extensions;
using System.Windows.Forms;

namespace SecondLaboratory.Views.Calculator
{
    public partial class StandartCalculatorForm : Form
    {
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
    }
}
