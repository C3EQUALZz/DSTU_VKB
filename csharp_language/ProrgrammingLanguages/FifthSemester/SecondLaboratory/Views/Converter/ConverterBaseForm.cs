using System;
using System.Windows.Forms;

namespace SecondLaboratory.Views.Converter;
public partial class ConverterBaseForm : Form
{
    protected Func<double, double> modifier = x => 2 * x;
    protected string LTitle = "LTitle";
    protected string RTitle = "RTitle";

    private short selectedSide = 0;

    public ConverterBaseForm()
    {
        InitializeComponent();
    }

    protected override void OnLoad(EventArgs e)
    {
        base.OnLoad(e);

        LTitleLabel.Text = LTitle;
        RTitleLabel.Text = RTitle;

        LValueLabel.Text = "0";
        RValueLabel.Text = "0";

        UpdateUI();
    }

    private void UpdateUI()
    {
        if (selectedSide == 0)
        {
            LValueLabel.Font = new System.Drawing.Font(LValueLabel.Font, System.Drawing.FontStyle.Bold);
        }
        else
        {
            RValueLabel.Font = new System.Drawing.Font(RValueLabel.Font, System.Drawing.FontStyle.Bold);
        }
    }
    private void ClearValue()
    {
        if (selectedSide == 0)
        {
            LValueLabel.Text = "0";
        }
        else
        {
            RValueLabel.Text = "0";
        }
    }
    private void UpdateValues()
    {

    }
    private void RemoveDigit()
    {
        if (selectedSide == 0)
        {
            if (LValueLabel.Text.Length < 2)
            {
                LValueLabel.Text = "0";
            }
            else
            {
                LValueLabel.Text = LValueLabel.Text.Substring(0, LValueLabel.Text.Length - 1);
            }
        }
        else
        {
            if (RValueLabel.Text.Length < 2)
            {
                RValueLabel.Text = "0";
            }
            else
            {
                RValueLabel.Text = RValueLabel.Text.Substring(0, RValueLabel.Text.Length - 1);
            }
        }
    }
    private void AddDigit(string digit)
    {
        if (selectedSide == 0)
        {
            if (LValueLabel.Text == "0" && digit != ",")
            {
                LValueLabel.Text = digit;
            }
            else
            {
                if (digit == "," && LValueLabel.Text.Contains(digit))
                {
                    return;
                }
                LValueLabel.Text += digit;
            }
        }
        else
        {
            if (RValueLabel.Text == "0" && digit != ",")
            {
                RValueLabel.Text = digit;
            }
            else
            {
                if (digit == "," && RValueLabel.Text.Contains(digit))
                {
                    return;
                }
                RValueLabel.Text += digit;
            }
        }
    }

    private void DigitButton_Click(object sender, System.EventArgs e)
    {
        var digit = (sender as Button).Text;
        AddDigit(digit);


    }
    private void BackspaceButton_Click(object sender, EventArgs e)
    {
        RemoveDigit();
    }
    private void CEButton_Click(object sender, EventArgs e)
    {
        ClearValue();
    }
}
