using System.Runtime.InteropServices;
using System;
using System.Windows.Forms;

using SecondLaboratory.Extensions;
using SecondLaboratory.Views.Calculator;
using SecondLaboratory.Services;

namespace SecondLaboratory; 
public partial class ShellForm : Form
{
    public static NavigationService NavigationService { get; private set; }

    public ShellForm()
    {
        InitializeComponent();

        NavigationService = new NavigationService();

        NavigationService.Navigated += (i) =>
        {
            PageTitleLabel.Text = i.Title;
        };
    }

    private void ShellForm_Load(object sender, System.EventArgs e)
    {
        // Commented bc of weird dynamic window resizing
        //panel3.SetRoundedShape(10, 10, 1, 1);

        NavigationPanel.Width = 0;

        NavigationItemsPanel.AutoScroll = true;

        button1.SetRoundedShape(5);

        PageTitleLabel.Text = "<PageTitle>";

        NavigationService.SetNavigationContainer(CalculatorContainerPanel);
        NavigationService.SetNavigationItemsContainer(NavigationItemsPanel);

        NavigationService.Configure();

        NavigationService.Navigate<StandartCalculatorForm>();
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
    }
}
