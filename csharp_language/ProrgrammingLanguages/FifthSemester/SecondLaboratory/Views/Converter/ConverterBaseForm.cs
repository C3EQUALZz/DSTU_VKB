using System;
using System.Windows.Forms;

namespace SecondLaboratory.Views.Converter;
public partial class ConverterBaseForm : Form
{
    protected Func<double, double> modifier = x => 2 * x;
    protected string LTitle = "LTitle";
    protected string RTitle = "RTitle";

    public ConverterBaseForm()
    {
        InitializeComponent();
    }

    protected override void OnLoad(EventArgs e)
    {
        base.OnLoad(e);

        LTitleLabel.Text = LTitle;
        RTitleLabel.Text = RTitle;
    }

    private void DigitButton_Click(object sender, System.EventArgs e)
    {
        var digit = (sender as Button).Text;
    }
}
