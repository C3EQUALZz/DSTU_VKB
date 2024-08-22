using SecondLaboratory.Models;
using SecondLaboratory.Core.Interfaces;
using SecondLaboratory.Presenters;

namespace SecondLaboratory.Views;

public partial class CalculatorView : Form, ICalculatorView
{
    private readonly CalculatorPresenter _presenter;

    public CalculatorView()
    {
        InitializeComponent();
        _presenter = new CalculatorPresenter(this, new CalculatorModel());
    }

    public string Display1Text
    {
        get => textDisplay1.Text;
        set => textDisplay1.Text = value;
    }

    public string Display2Text
    {
        get => textDisplay2.Text;
        set => textDisplay2.Text = value;
    }

    public bool EnterValue { get; set; }
    public string? Operation { get; set; }
    public string? FirstNumber { get; set; }
    public string? SecondNumber { get; set; }
    public double Result { get; set; }

    public void AppendHistory(string text)
    {
        richTextBoxDisplayHistory.AppendText(text);
    }

    public void ClearHistory()
    {
        richTextBoxDisplayHistory.Clear();
        if (richTextBoxDisplayHistory.Text == string.Empty)
        {
            richTextBoxDisplayHistory.Text = "История операций пуста";
        }
    }

    public void ToggleHistoryPanel()
    {
        panelHistory.Height = (panelHistory.Height == 5) ? 355 : 5;
    }


    private void OnNumberButtonClick(object sender, EventArgs e)
    {
        _presenter.OnNumberButtonClick(sender, e);
    }

    private void OnMathOperationButtonClick(object sender, EventArgs e)
    {
        _presenter.OnMathOperationButtonClick(sender, e);
    }

    private void OnEqualsButtonClick(object sender, EventArgs e)
    {
        _presenter.OnEqualsButtonClick(sender, e);
    }

    private void OnHistoryButtonClick(object sender, EventArgs e)
    {
        _presenter.OnHistoryButtonClick(sender, e);
    }

    private void OnClearHistoryButtonClick(object sender, EventArgs e)
    {
        _presenter.OnClearHistoryButtonClick(sender, e);
    }

    private void OnBackSpaceButtonClick(object sender, EventArgs e)
    {
        _presenter.OnBackSpaceButtonClick(sender, e);
    }

    private void OnClearButtonClick(object sender, EventArgs e)
    {
        _presenter.OnClearButtonClick(sender, e);
    }

    private void OnClearEntryButtonClick(object sender, EventArgs e)
    {
        _presenter.OnClearEntryButtonClick(sender, e);
    }

    private void OnOperationButtonsClick(object sender, EventArgs e)
    {
        _presenter.OnOperationButtonClick(sender, e);
    }

    private void OnButtonExitClick(object sender, EventArgs e)
    {
        Application.Exit();
    }
}
