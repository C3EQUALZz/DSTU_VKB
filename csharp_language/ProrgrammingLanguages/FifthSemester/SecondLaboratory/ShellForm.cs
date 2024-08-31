using System.Runtime.InteropServices;
using System;
using System.Windows.Forms;

using SecondLaboratory.Extensions;

namespace SecondLaboratory; 
public partial class ShellForm : Form
{
    public ShellForm()
    {
        InitializeComponent();
    }

    private void ShellForm_Load(object sender, System.EventArgs e)
    {
        //panel3.SetRoundedShape(10, 10, 1, 1);
        panel3.Width = 0;

        panel3.AutoScroll = true;

        button1.SetRoundedShape(5);

        var converterButtons = new Button[]
        {
            StandartCalculatorButton,
            button2,
            button3,
            button4,
            button5,
            button6,
            button7,
            button8,
            button9,
            button10,
            button11,
            button12,
            button13,
            button14,
            button15,
            button16,
            button17,
            button18,
            button19,
            button20,
        };

        foreach (var button in converterButtons)
        {
            button.SetRoundedShape(10);
        }

        PageTitleLabel.Text = "There must be page title";
    }

    [DllImport("DwmApi")] //System.Runtime.InteropServices
    private static extern int DwmSetWindowAttribute(IntPtr hwnd, int attr, int[] attrValue, int attrSize);

    protected override void OnHandleCreated(EventArgs e)
    {
        if (DwmSetWindowAttribute(Handle, 19, new[] { 1 }, 4) != 0)
            DwmSetWindowAttribute(Handle, 20, new[] { 1 }, 4);
    }

    private void button1_Click(object sender, EventArgs e)
    {
        panel3.Width = panel3.Width == 0 ? 275 : 0;
        Console.WriteLine(panel3.Width);
    }
}
