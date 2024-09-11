using System;
using System.Windows.Forms;

namespace SecondLaboratory.Views.Converter;
public partial class ConverterBaseForm : Form
{
    protected Func<double, double> modifier = x => 2 * x;

    public ConverterBaseForm()
    {
        InitializeComponent();
    }

    private void DigitButton_Click(object sender, System.EventArgs e)
    {
        var digit = (sender as Button).Text;
    }
}
