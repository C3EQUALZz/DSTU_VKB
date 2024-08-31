using System.Runtime.InteropServices;
using System;
using System.Windows.Forms;

using SecondLaboratory.Extensions;
using SecondLaboratory.Views.Calculator;

namespace SecondLaboratory; 
public partial class ShellForm : Form
{
    public ShellForm()
    {
        InitializeComponent();
    }

    private void ShellForm_Load(object sender, System.EventArgs e)
    {
        // Commented bc of weird dynamic window resizing
        //panel3.SetRoundedShape(10, 10, 1, 1);

        NavigationPanel.Width = 0;

        NavigationItemsPanel.AutoScroll = true;

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

        PageTitleLabel.Text = "<PageTitle>";

        var calcForm = new StandartCalculatorForm();
        calcForm.TopLevel = false;
        calcForm.Dock = DockStyle.Fill;

        CalculatorContainerPanel.Controls.Add(calcForm);
        calcForm.Show();
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
        NavigationPanel.Width = NavigationPanel.Width == 0 ? 250 : 0;
        Console.WriteLine(NavigationPanel.Width);
    }
}
